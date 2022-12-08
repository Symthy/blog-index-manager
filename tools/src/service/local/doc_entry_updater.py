from domain.doc.doc_entry import DocEntries, DocEntry
from domain.doc.doc_entry_builder import DocEntryBuilder
from dump.interface import IDumpEntriesAccessor
from service.local.doc_entry_summary_writer import DocEntrySummaryWriter


class DocEntryUpdater:
    def __init__(self, dump_doc_data_accessor: IDumpEntriesAccessor[DocEntries, DocEntry],
                 doc_entry_summary_writer: DocEntrySummaryWriter):
        self.__dump_doc_data_accessor = dump_doc_data_accessor
        self.__doc_entry_summary_writer = doc_entry_summary_writer

    def update_pickup(self, doc_entry_id: str, pickup: bool):
        entry: DocEntry = self.__dump_doc_data_accessor.load_entry(doc_entry_id)
        builder = DocEntryBuilder(entry).pickup(pickup)
        updated_entry = builder.build()
        self.__dump_doc_data_accessor.save_entry(updated_entry)
        self.__doc_entry_summary_writer.update_file()
