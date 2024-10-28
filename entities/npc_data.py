from dataclasses import dataclass
from typing import List

@dataclass
class NPCData:
    name: str
    age: int
    role: str
    chat_messages: List[str]

    @classmethod
    def create_preset_npcs(cls) -> dict:
        """Create a dictionary of preset NPCs with their data"""
        return {
            "butler": cls(
                name="James",
                age=55,
                role="Butler",
                chat_messages=[
                    "Would you like some tea?",
                    "Everything must be in perfect order.",
                    "I'll make sure the house is spotless.",
                    "Time to dust the furniture.",
                    "The silver needs polishing.",
                    "Dinner will be served at 7.",
                ]
            ),
            "maid": cls(
                name="Clara",
                age=32,
                role="Maid",
                chat_messages=[
                    "These windows need cleaning.",
                    "Time to change the bedsheets.",
                    "The living room looks lovely now.",
                    "Where did I put the duster?",
                    "The garden looks beautiful today.",
                    "Everything should be neat and tidy.",
                ]
            ),
            "gardener": cls(
                name="Tom",
                age=45,
                role="Gardener",
                chat_messages=[
                    "The roses are blooming nicely.",
                    "Time to water the plants.",
                    "These hedges need trimming.",
                    "Perfect weather for gardening.",
                    "The flowers look gorgeous today.",
                    "Need to check on the vegetables.",
                ]
            ),
            "chef": cls(
                name="Maria",
                age=38,
                role="Chef",
                chat_messages=[
                    "What shall I prepare for dinner?",
                    "The kitchen needs restocking.",
                    "This recipe needs perfecting.",
                    "Time to prepare lunch.",
                    "These ingredients are so fresh!",
                    "I love cooking in this kitchen.",
                ]
            )
        }