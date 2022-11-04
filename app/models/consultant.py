from neomodel import StructuredNode, StringProperty, RelationshipTo

class Consultant(StructuredNode):
    Name = StringProperty()
    skills = RelationshipTo(".skill.Skill", "KNOWS")
