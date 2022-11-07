from neomodel import StructuredNode, StringProperty, RelationshipFrom

class Skill(StructuredNode):
    Name = StringProperty()
    Group = StringProperty()
    consultants = RelationshipFrom(".consultant.Consultant", "KNOWS")
