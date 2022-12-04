from common.constant import LOCAL_DOCS_ENTRY_INDEX_RESULT_PATH
from files.file_accessor import write_text_lines
from service.entry_summary_factory import EntrySummaryFactory


def update_doc_entry_summary_file(entry_summary_factory: EntrySummaryFactory):
    entry_summary = entry_summary_factory.build_doc_entry_summary()
    write_text_lines(LOCAL_DOCS_ENTRY_INDEX_RESULT_PATH, entry_summary.pickup_and_all_entry_lines())
