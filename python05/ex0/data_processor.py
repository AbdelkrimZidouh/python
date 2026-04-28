import abc
import typing


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._total: int = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("Nexus Buffer Empty")
        rank = self._total - len(self._storage)
        value = self._storage.pop(0)
        return (rank, value)


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)
        return False

    def ingest(
        self,
        data: typing.Union[
            int,
            float,
            list[int],
            list[float],
            list[typing.Union[int, float]]
        ]
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(str(item))
                self._total += 1
        else:
            self._storage.append(str(data))
            self._total += 1


class TextProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(
        self,
        data: typing.Union[str, list[str]]
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(item)
                self._total += 1
        else:
            self._storage.append(data)
            self._total += 1


class LogProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            )
        if isinstance(data, list):
            return all(
                isinstance(d, dict) and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in d.items()
                )
                for d in data
            )
        return False

    def ingest(
        self,
        data: typing.Union[dict[str, str], list[dict[str, str]]]
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        if isinstance(data, list):
            for item in data:
                entry = f"{item['log_level']}: {item['log_message']}"
                self._storage.append(entry)
                self._total += 1
        else:
            entry = f"{data['log_level']}: {data['log_message']}"
            self._storage.append(entry)
            self._total += 1


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    num_proc = NumericProcessor()

    print(f" Trying to validate input '42': {num_proc.validate(42)}")
    print(f" Trying to validate input 'Hello': {num_proc.validate('Hello')}")

    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num_proc.ingest("foo")
    except TypeError as e:
        print(f" Got exception: {e}")

    data_num = [1, 2, 3, 4, 5]
    print(f" Processing data: {data_num}")
    num_proc.ingest(data_num)
    print(" Extracting 3 values...")
    for _ in range(3):
        rank, val = num_proc.output()
        print(f" Numeric value {rank}: {val}")

    print("\nTesting Text Processor...")
    txt_proc = TextProcessor()

    print(f" Trying to validate input '42': {txt_proc.validate(42)}")

    data_txt = ['Hello', 'Nexus', 'World']
    print(f" Processing data: {data_txt}")
    txt_proc.ingest(data_txt)
    print(" Extracting 1 value...")
    rank, val = txt_proc.output()
    print(f" Text value {rank}: {val}")

    print("\nTesting Log Processor...")
    log_proc = LogProcessor()

    print(f" Trying to validate input 'Hello': {log_proc.validate('Hello')}")

    data_log = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    print(f" Processing data: {data_log}")
    log_proc.ingest(data_log)
    print(" Extracting 2 values...")
    for _ in range(2):
        rank, val = log_proc.output()
        print(f" Log entry {rank}: {val}")
