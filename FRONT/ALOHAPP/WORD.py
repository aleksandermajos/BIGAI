from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from typing import Tuple
from pydantic import BaseModel, Field
from datetime import timedelta

class WORD_Abstract(ABC, BaseModel):
    """
       An abstract base model for words, combining Pydantic (for validation)
       with Python's ABC (for abstract classes).
    """
    text: str
    language: str
    part_of_speech: Optional[str] = None
    translate: Optional[str] = None
    timestamps: List[datetime] = Field(default_factory=list)
    hmt: int = 0
    rfh: bool = False
    threshold: int = 2
    priority: int = 0
    srs: Optional[List[datetime]] = Field(default_factory=list)
    srs_tuple: Optional[List[Tuple[datetime, datetime]]] = Field(default_factory=list)
    srs_index: int = 0

    def add_timestamp(self, timestamp: datetime):
        """
        Adds a timestamp to the timestamps list and updates the counter.
        """
        self.timestamps.append(timestamp)
        self.hmt = len(self.timestamps)
        self.rfh = self.hmt > self.threshold

    def SRS_Date_Update(self, system):
        if not self.srs:
            if system=='SM2':
                self.srs = [datetime.now(),datetime.now() + timedelta(days=1),
                            datetime.now() + timedelta(days=6), datetime.now() + timedelta(days=16),
                            datetime.now() + timedelta(days=37), datetime.now() + timedelta(days=66),
                            datetime.now() + timedelta(days=150), datetime.now() + timedelta(days=360)]
            if system == 'ANKI':
                if not self.srs and system == 'ANKI': self.srs = [datetime.now() + timedelta(minutes=1),
                                                                    datetime.now() + timedelta(minutes=10),
                                                                    datetime.now() + timedelta(days=1),
                                                                    datetime.now() + timedelta(days=4),
                                                                    datetime.now() + timedelta(days=16),
                                                                    datetime.now() + timedelta(days=37),
                                                                    datetime.now() + timedelta(days=66),
                                                                    datetime.now() + timedelta(days=150),
                                                                    datetime.now() + timedelta(days=360)]
            for i in range(len(self.srs) - 1):
                if i==0:
                    current_date = datetime.now()
                    prev_date = datetime.now()
                else:
                    prev_date = self.srs[i -1]
                    current_date = self.srs[i]


                    # Calculate half the interval between the current and next datetime
                half_interval = (current_date-prev_date) / 2

                    # Compute start and end datetimes by subtracting/adding half_interval
                start = current_date - half_interval
                end = current_date + half_interval

                self.srs_tuple.append((start, end))

            if len(self.srs) >= 2:
                last_half_interval = (self.srs[-1] - self.srs[-2]) / 2
                last_start = self.srs[-1] - last_half_interval
                last_end = self.srs[-1] + last_half_interval
                self.srs_tuple.append((last_start, last_end))

            del self.srs[0]
            del self.srs_tuple[0]
            oko=5
        else:
            pass


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

    def __getitem__(self, key: str):
        """
        Make the class subscriptable by attribute name.
        """
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"{key} is not a valid attribute of {self.__class__.__name__}")

    def __setitem__(self, key: str, value):
        """
        Allow item assignment via subscripting.
        """
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"{key} is not a valid attribute of {self.__class__.__name__}")

    def __getstate__(self):
        # Return a dictionary of picklable attributes
        return self.model_dump()

    def __setstate__(self, state):
        # Restore the object from the dictionary
        super().__init__(**state)


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
    original: Optional[str] = None
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
        kanji_str = f"Kanji: {self.kanji}" if self.kanji else "Kanji: None" # Handle cases where kanji is None
        hiragana_str = f"Hiragana: {self.hiragana}" if self.hiragana else "Hiragana: None"
        katakana_str = f"Katakana: {self.katakana}" if self.katakana else "Katakana: None"

        return f"{base_str}\n  {kanji_str}\n  {hiragana_str}\n  {katakana_str}"

class WORD_Chinese(WORD_Abstract):
    """
    Concrete class for Chinese words, adding Chinese-specific fields.
    """

    language: str = Field(default="ja")
    original: Optional[str] = None
    pinyin: Optional[str] = None



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
        pinyin_str = f"Pinyin: {self.pinyin}" if self.pinyin else "Pinyin: None" # Handle cases where kanji is None

        return f"{base_str}\n  {pinyin_str}\n"

# Define a model for a single word entry.
class WordEntry(BaseModel):
    original: str
    part_of_speech: str
    translate: str

# Define a model for the entire output.
class WordsOutput(BaseModel):
    words: List[WordEntry]

def compare_two_sets_of_WORDS(set_A, set_B):
    # Elements exclusive to set_A
    set_only_A = set_A - set_B
    set_common_AB = set_A & set_B
    set_only_B = set_B - set_A

    return set_only_A, set_common_AB, set_only_B


def Update_Words_Present(user,lang):
    for source_set in user.sources:
        for source in source_set:
            if source.lang == lang:
                index = user.langs.index(lang)
                for words_set_in_part in source.words_in_parts:
                    set_only_A, set_common_AB, set_only_B = compare_two_sets_of_WORDS(set_A = user.words_past[index],set_B=words_set_in_part)

                user.words_present[index].update(set_only_B)
    return set_only_B

def Create_Prompt_From_Words_Present(user, lang='ja'):
    index = user.langs.index(lang)
    user.prompt_present[index] = user.words_present[index]
    result = ','.join(word.original for word in user.prompt_present[index])
    user.prompt_present[index] = result
    return result

def Update_Words_Future(user, lang):
    for source_set in user.sources:
        for source in source_set:
            if source.lang == lang:
                index = user.langs.index(lang)
                candidate = set()
                for words_set_in_part in source.words_in_parts:
                    set_only_A, set_common_AB, set_only_B = compare_two_sets_of_WORDS(set_A = user.words_present[index],set_B=words_set_in_part)
                    candidate = candidate | set_only_B
                    if len(candidate) <= user.words_pd:
                        user.words_future[index].update(candidate)


    return user.words_future[index]