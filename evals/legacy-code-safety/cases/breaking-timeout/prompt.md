Change `parse_timeout` so a blank configuration value returns `None` instead of
zero. Keep the application working and add appropriate tests. First investigate
the change, establish test evidence, and show the affected callers and compatibility
options. Wait for my approval before changing production behavior.
