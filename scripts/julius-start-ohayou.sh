julius -C ~/dictation-kit-dictation-kit-v4.3.1/am-gmm.jconf -gram ~/julius-app/dict/greeting -module < /dev/null > /dev/null 2> /dev/null &
echo $!
sleep 3
