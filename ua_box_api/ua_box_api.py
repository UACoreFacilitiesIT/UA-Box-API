from io import BytesIO
import boxsdk

__author__ = "Stephen Stern"
__maintainer__ = "Stephen Stern"
__email__ = "sterns1@email.arizona.edu"


class BoxApi:
    def __init__(self, stache_secret):
        # Authenticate the API client using the JWT authentication method.
        private_key_stream = BytesIO(
            stache_secret["boxAppSettings"]["appAuth"]["privateKey"].encode())
        jwt_options = {
            "client_id": stache_secret["boxAppSettings"]["clientID"],
            "client_secret": stache_secret["boxAppSettings"]["clientSecret"],
            "enterprise_id": stache_secret["enterpriseID"],
            "jwt_key_id": stache_secret[
                "boxAppSettings"]["appAuth"]["publicKeyID"],
            "rsa_private_key_passphrase": stache_secret[
                "boxAppSettings"]["appAuth"]["passphrase"].encode(),
            "rsa_private_key_data": private_key_stream
        }
        auth = boxsdk.JWTAuth(**jwt_options)
        auth.authenticate_instance()
        self.client = boxsdk.Client(auth)

    def get_all_items(self, item_id):
        """Returns list of all items in the object with the given item_id."""
        # If a folder is passed in, it gets caught in an infinite while loop
        # with a bare except somewhere -- instead, check that the id is an int.
        if not (isinstance(item_id, int) or isinstance(item_id, str)):
            raise TypeError("Item_id must be an int.")
        folder = self.client.folder(folder_id=item_id)

        items = list()
        offset = 0
        has_next_item = True

        # Every 300000 items, get a new generator; otherwise, add the current
        # generator's next(). If the current generator doesn't have a next(),
        # make while condition False.
        while has_next_item:
            if len(items) == offset:
                items_generator = folder.get_items(
                    limit=offset + 300000, offset=offset)
                offset += 300000
            try:
                items.append(items_generator.next())
            except StopIteration:
                has_next_item = False

        return items

    def find_child_by_name(self, name, item_id):
        """Returns object with name if found in item_id, or None if not."""
        matches = [x for x in self.get_all_items(item_id) if x.name == name]
        if matches:
            return matches[0]
        return None

    def get_duplicate_file_name(self, folder_id, current_name, zip_file=False):
        """If the given name is in the folder, return a modified file name."""
        search_name = current_name
        if zip_file:
            search_name = current_name.replace(".zip", "")
        folder_items = self.get_all_items(folder_id)
        duplicates = [
            item.name for item in folder_items if search_name in item.name]

        if duplicates:
            if zip_file:
                return f"{search_name}({len(duplicates)}).zip"

            return f"{current_name}({len(duplicates)})"

        return current_name
