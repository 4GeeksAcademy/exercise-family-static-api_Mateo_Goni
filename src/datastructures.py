"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        membersRequest = [
            {"id": self._generateId(), "first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]},
            {"id": self._generateId(), "first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]},
            {"id": self._generateId(), "first_name": "Jimmy", "age": 5, "lucky_numbers": [1]}
        ]


        self.last_name = last_name

        # example list of members
        self._members = membersRequest

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        member_id = member.get('id', self._generateId())
        member['id'] = member_id
        self._members.append(member)

    def delete_member(self, id):
        self._members = [member for member in self._members if member['id'] != id]

    def update_member(self, member):
        for i, existing_member in enumerate(self._members):
            if existing_member['id'] == member['id']:
                self._members[i] = member
                return True
        return False

    def get_member(self, id):
        for member in self._members:
            if member['id'] == id:
                return member
        return None

    def get_all_members(self):
        return self._members