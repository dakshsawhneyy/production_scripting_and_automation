### Scenario: 
- Our build servers are running out of disk space. 
- Developers leave node_modules, venv, and build folders everywhere. 

If we just run rm -rf, we might delete active projects. 

We need a Reporter first.

#### finder.sh - Scans the filesystem. It is 100x faster than Python at walking directories.
#### analyzer.py - Takes that raw list, calculates exact sizes, checks who owns them, and generates a JSON Report for the manager to approve.