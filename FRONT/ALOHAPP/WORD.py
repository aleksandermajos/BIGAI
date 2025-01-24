from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel, Field

class WORD_Abstract(ABC, BaseModel):
    """
       An abstract base model for words, combining Pydantic (for validation)
       with Python's ABC (for abstract classes).
    """
    text: str
    language: str
    part_of_speech: Optional[str] = None

    @abstractmethod
    def lemmatize(self) -> str:
        """
        Abstract method that derived classes must implement.
        """
        pass

    def __str__(self) -> str:
        return f"[{self.language}] {self.text} - POS: {self.part_of_speech}"

    def __hash__(self) -> int:
        return hash((self.text, self.language, self.part_of_speech))

    def __eq__(self, other) -> bool:
        if not isinstance(other, WORD_Abstract):
            return NotImplemented
        return (
                self.text == other.text and
                self.language == other.language and
                self.part_of_speech == other.part_of_speech
        )

class WORD_English(WORD_Abstract):
    """
    Concrete class for English words, implementing 'lemmatize'.
    """


    language: str = Field(default="en")

    def lemmatize(self) -> str:
        return self.text


class WORD_Japanese(WORD_Abstract):
    """
    Concrete class for Japanese words, adding Japanese-specific fields.
    """

    language: str = Field(default="ja")
    orginal: Optional[str] = None
    hiragana: Optional[str] = None
    katakana: Optional[str] = None
    hepburn: Optional[str] = None
    kunrei: Optional[str] = None
    passport: Optional[str] = None


    def lemmatize(self) -> str:
        """
        A dummy lemmatizer for Japanese words.
        Integrate with MeCab, SudachiPy, etc., for real usage.
        """
        # Return the 'text' or 'kanji' as a placeholder
        return self.text

    def __str__(self) -> str:
        """
        Provide more descriptive string for Japanese words.
        """
        base_str = super().__str__()
        return f"{base_str}\n  Kanji: {self.kanji}\n  Hiragana: {self.hiragana}\n  Katakana: {self.katakana}"
