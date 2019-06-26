curl  -D- \
   -u username:password \
   -X POST \
   -H "Content-Type: application/json" \
   https://jira/rest/api/2/issue/ \
   --data "@/Users/jhecht/Desktop/data.txt"
