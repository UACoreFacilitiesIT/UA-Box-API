from box_sdk_gen import (
    BoxClient,
    BoxJWTAuth,
    FileFull,
    FolderFull,
    FolderMini,
    JWTConfig,
    WebLink,
)

__author__ = "Stephen Stern"
__maintainer__ = "Stephen Stern"
__email__ = "sterns1@email.arizona.edu"


class BoxApi:
    def __init__(self, stache_secret):
        # Authenticate the API client using the JWT authentication method.
        jwt_config = JWTConfig(
            client_id=stache_secret["boxAppSettings"]["clientID"],
            client_secret=stache_secret["boxAppSettings"]["clientSecret"],
            enterprise_id=stache_secret["enterpriseID"],
            jwt_key_id=stache_secret["boxAppSettings"]["appAuth"]["publicKeyID"],
            private_key=stache_secret["boxAppSettings"]["appAuth"]["privateKey"],
            private_key_passphrase=stache_secret["boxAppSettings"]["appAuth"][
                "passphrase"
            ],
        )
        auth = BoxJWTAuth(config=jwt_config)
        self.client = BoxClient(auth=auth)

    def get_all_items(self, item_id: str) -> list[FileFull | FolderMini | WebLink]:
        """Returns list of all items in the object with the given item_id."""
        folder = self.client.folders.get_folder_items(folder_id=item_id, usemarker=True)
        items = folder.entries
        next_item = folder.next_marker
        while next_item is not None:
            folder = self.client.folders.get_folder_items(
                folder_id=item_id, usemarker=True, marker=next_item
            )
            if folder.entries is not None:
                items += folder.entries
                next_item = folder.next_marker
            else:
                break

        if items is None:
            raise FileNotFoundError("Failed to find requested folder.")
        else:
            return items

        """Returns object with name if found in item_id, or None if not."""
    def find_child_by_name(
        self, name: str, item_id: str
    ) -> FileFull | FolderFull | WebLink:
        search = self.client.search.search_for_content(
            query=f'"{name}"',  # Wrap query in double quotes, because Box API.
            ancestor_folder_ids=[str(item_id)],
            content_types=["name"],
        )

        # This construct throws a ValueError if there isn't exactly 1 match.
        # https://stackoverflow.com/a/7008062
        # https://dbader.org/blog/python-nested-unpacking
        [result] = [item for item in search.entries if item.name == name]
        return result

        # This block would be reasonable for the first of one or more matches.
        # Could also do all results? Then we could use get_duplicate_file_name.
        # But now we'd be returning a list instead of a
        # FileFull | FolderFull | WebLink | SearchResultWithSharedLink

        # result = next((item for item in search.entries if item.name == name), None)
        # if result:
        #     return result
        # else:
        #     raise FileNotFoundError("Failed to find requested item.")

    def get_duplicate_file_name(
        self, folder_id: str, name: str, zip_file: bool = False
    ) -> str:
        """If the given name is in the folder, return a modified file name."""
        if zip_file:
            name = name.replace(".zip", "")
        folder_items = self.get_all_items(folder_id)
        duplicates = [item.name for item in folder_items if name in item.name]

        if duplicates:
            if zip_file:
                return f"{name}({len(duplicates)}).zip"

            return f"{name}({len(duplicates)})"

        return name
