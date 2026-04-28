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
        rank = self._total - len(self._storage)
        value = self._storage.pop(0)
        return (rank, value)

    def remaining(self) -> int:
        return len(self._storage)

    def total(self) -> int:
        return self._total


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return bool(data) and all(
                isinstance(x, (int, float)) for x in data
            )
        return False

    def ingest(
        self,
        data: typing.Union[int, float, list[typing.Union[int, float]]]
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
            return bool(data) and all(isinstance(x, str) for x in data)
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
            return bool(data) and all(
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
        if isinstance(data, dict):
            entry = f"{data['log_level']}: {data['log_message']}"
            self._storage.append(entry)
            self._total += 1
        else:
            for item in data:
                entry = f"{item['log_level']}: {item['log_message']}"
                self._storage.append(entry)
                self._total += 1


class ExportPlugin(typing.Protocol):
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        ...


class CSVExportPlugin:
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        if not data:
            return
        row = ",".join(value for _, value in data)
        print(f"CSV Output:\n{row}")


class JSONExportPlugin:
    def process_output(
        self, data: list[tuple[int, str]]
    ) -> None:
        if not data:
            return
        pairs = ", ".join(
            f'"item_{rank}": "{value}"' for rank, value in data
        )
        print("JSON Output:\n" + "{" + pairs + "}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for element in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            if not handled:
                print(
                    f"DataStream error - "
                    f"Can't process element in stream: {element}"
                )

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        names = {
            NumericProcessor: "Numeric Processor",
            TextProcessor: "Text Processor",
            LogProcessor: "Log Processor",
        }
        for proc in self._processors:
            name = names.get(type(proc), type(proc).__name__)
            print(
                f"{name}: total {proc.total()} items processed, "
                f"remaining {proc.remaining()} on processor"
            )

    def output_pipeline(
        self, nb: int, plugin: ExportPlugin
    ) -> None:
        for proc in self._processors:
            collected: list[tuple[int, str]] = []
            count = min(nb, proc.remaining())
            for _ in range(count):
                collected.append(proc.output())
            plugin.process_output(collected)


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===")

    print("\nInitialize Data Stream...\n")
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Processors")
    ds.register_processor(NumericProcessor())
    ds.register_processor(TextProcessor())
    ds.register_processor(LogProcessor())

    batch1 = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {'log_level': 'WARNING',
             'log_message': 'Telnet access! Use ssh instead'},
            {'log_level': 'INFO',
             'log_message': 'User wil is connected'}
        ],
        42,
        ['Hi', 'five']
    ]
    print(f"\nSend first batch of data on stream: {batch1}")
    ds.process_stream(batch1)
    ds.print_processors_stats()

    csv_plugin = CSVExportPlugin()
    print("\nSend 3 processed data from each processor to a CSV plugin:")
    ds.output_pipeline(3, csv_plugin)
    ds.print_processors_stats()

    batch2 = [
        21,
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [
            {'log_level': 'ERROR', 'log_message': '500 server crash'},
            {'log_level': 'NOTICE',
             'log_message': 'Certificate expires in 10 days'}
        ],
        [32, 42, 64, 84, 128, 168],
        'World hello'
    ]
    print(f"\nSend another batch of data: {batch2}")
    ds.process_stream(batch2)
    ds.print_processors_stats()

    json_plugin = JSONExportPlugin()
    print("\nSend 5 processed data from each processor to a JSON plugin:")
    ds.output_pipeline(5, json_plugin)
    ds.print_processors_stats()
