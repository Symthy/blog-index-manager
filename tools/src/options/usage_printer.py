USAGE_CONTENT = """Document and Blog Entry Manager

USAGE:
  <command> [OPTIONS]

OPTIONS:
  -i, -init                            initialize docs directory (don't delete exist file and dir).
  -n, -new [<OPTS>]                    new document set under "work" dir (create dir, md file and category file).
    OPTS (can also specify the following together):                                
      -t, -title <DocTitle>              specified document title (default: "Document").
      -c, -category <CategoryName>       specified category (default: empty value).
  -s, -search <Keyword>                specifiable keyword: Group Name, Category Name, Title Keyword(partial match).
  -p, -push [<OPTS>] <DirName>         push document set from "work" dir to "docs" dir.
    OPTS: -a, -all                       in addition to the above, post your blog.
  -r, -retrieve [<OPTS>] <DocEntryID>  retrieve document set from "docs" dir to "work" dir (and backup).
    OPTS: -c, -cancel                    cancel retrieve (move the backup back to "docs" dir).
  -b, -blog <OPTS>                     operation to your blog.
    OPTS (can't also specify the following together):                                
      -c, -collect                       collect all blog entries from your blog. 
      -p, -push <DocEntryID>             post specified document to your blog.
  -h, -help                            show usage.
"""


def print_usage():
    print(USAGE_CONTENT)
