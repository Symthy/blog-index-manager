from common.constant import LOCAL_DOCS_ENTRY_INDEX_RESULT_PATH
from files.file_accessor import write_text_lines
from service.entry_summary_factory import EntrySummaryFactory


class DocEntrySummaryWriter:
    def __init__(self, entry_summary_factory: EntrySummaryFactory):
        self.__entry_summary_factory: EntrySummaryFactory = entry_summary_factory

    def update_file(self):
        entry_summary = self.__entry_summary_factory.build_doc_entry_summary()
        write_text_lines(LOCAL_DOCS_ENTRY_INDEX_RESULT_PATH, entry_summary.pickup_and_all_entry_lines)
