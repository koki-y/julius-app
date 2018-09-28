iconv -f utf8 -t eucjp ~/julius-python/dictionary/greeting.yomi | ~/julius-4.4.2.1/gramtools/yomi2voca/yomi2voca.pl | iconv -f eucjp -t utf8 > ~/julius-python/dictionary/greeting.phone
