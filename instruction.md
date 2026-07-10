An Apache-style access log is available at /app/access.log. Parse it and produce the required summary report.

The result must satisfy all of the following:

1. Write /app/report.json as valid JSON containing one object with exactly these keys: "total_requests", "unique_ips", and "top_path".
2. "total_requests" must be an integer equal to the number of non-empty request lines in /app/access.log.
3. "unique_ips" must be an integer equal to the number of distinct client IP addresses, where the client IP is the first whitespace-separated field on each non-empty line.
4. "top_path" must be a string equal to the request path that occurs most often in the quoted HTTP request field, such as "/index.html".
5. Do not modify /app/access.log.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
