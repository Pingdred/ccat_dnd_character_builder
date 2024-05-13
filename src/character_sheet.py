import math
from pydantic import BaseModel, Field, validator, computed_field

class CharacterSheet(BaseModel):
    name: str = Field(description="The name of the character", min_length=1, max_length=50)
    race: str = Field(description="The race of the character. Valid values: Human, Elf, Dwarf, Halfling, Half-Orc, Half-Elf, Gnome, Tiefling", min_length=1, max_length=50)
    class_: str = Field(description="The class of the character. Valid values: Barbarian, Bard, Cleric, Druid, Fighter, Monk, Paladin, Ranger, Rogue, Sorcerer, Warlock, Wizard", min_length=1, max_length=50)
    level: int = Field(description="The level of the character. Must be between 1 and 20.")
    
    strength: int = Field(description="The strength score of the character. Must be between 1 and 30.", ge=1, le=30)
    dexterity: int = Field(description="The dexterity score of the character. Must be between 1 and 30.", ge=1, le=30)
    constitution: int = Field(description="The constitution score of the character. Must be between 1 and 30.", ge=1, le=30)
    intelligence: int = Field(description="The intelligence score of the character. Must be between 1 and 30.", ge=1, le=30)
    wisdom: int = Field(description="The wisdom score of the character. Must be between 1 and 30.", ge=1, le=30)
    charisma: int = Field(description="The charisma score of the character. Must be between 1 and 30.", ge=1, le=30)
    
    @computed_field
    @property
    def strength_modifier(self) -> int:
        return (self.strength - 10) // 2

    @computed_field
    @property
    def dexterity_modifier(self) -> int:
        return math.floor((self.dexterity - 10) / 2)
    
    @computed_field
    @property
    def constitution_modifier(self) -> int:
        return (self.constitution - 10) // 2
    
    @computed_field
    @property
    def intelligence_modifier(self) -> int:
        return (self.intelligence - 10) // 2
    
    @computed_field
    @property
    def wisdom_modifier(self) -> int:
        return (self.wisdom - 10) // 2

    @computed_field
    @property
    def charisma_modifier(self) -> int:
        return (self.charisma - 10) // 2
    
    health_points: int = Field(description="The health points of the character. Must be greater than 0.")
    armor_class: int = Field(description="The armor class of the character. Must be greater than 0.")

    @computed_field
    @property
    def proficiency_bonus(self) -> int:
        return self.level // 4 + 1 if self.level < 17 else 6

    @computed_field
    @property
    def initiative(self) -> int:
        return self.dexterity_modifier + self.proficiency_bonus


    @validator('race')
    def validate_race(cls, v):
        valid_races = ['Human', 'Elf', 'Dwarf', 'Halfling', 'Half-Orc', 'Half-Elf', 'Gnome', 'Tiefling']
        if v not in valid_races:
            raise ValueError(f"{v} is an invalid Race, valid races are: Human, Elf, Dwarf, Halfling, Half-Orc, Half-Elf, Gnome, Tiefling.")
        return v

    @validator('class_')
    def validate_class(cls, v):
        valid_classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
        if v not in valid_classes:
            raise ValueError(f"{v} is an invalid Class, valid Classes are: Barbarian, Bard, Cleric, Druid, Fighter, Monk, Paladin, Ranger, Rogue, Sorcerer, Warlock, Wizard.")
        return v

    @validator('level')
    def validate_level(cls, v):
        if v < 1 or v > 20:
            raise ValueError("Level must be between 1 and 20")
        return v
