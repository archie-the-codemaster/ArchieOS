# Archie OS!
## A simple, simulated operating system written in Python
This is a passion project of mine started because my friends bet me to code an OS simulator

## Current features
1. Fully functioning configuration system (Stores the data in JSON files).
2. System integrity check based on hashing (Uses SHA256 and stores in a JSON file).
3. Logon system based on user password preferences set during the configuration.
4. Basic system utilities (simple text editor, shutdown/reboot commands, clear command).
5. Cool progressbars!

## Work in progress
1. A simple package manager that pulls from GitHub (The bare bones are in the system already)
2. Simulated hardware such as RAM and storage (including SWAP memory)
3. A fetch tool akin to fasfetch (or hyfetch if I can pull it off)
## Bugs
As far as I have tested it, the code seems to be bugless, but if you find anything that breaks/crashes the program open an issue and describe how to replicate it alongside the error code it throws, I'll try to get it fixed

## Other notes
A rework is in progress as you can see by the remade.py file. I plan on remaking some aspects of the original file such as the config and boot sequence to make the code more readable/stable. That file is a WIP so DO NOT touch it!
Feel free to fork this project and put your own spin on ArchieOS, just make sure to credit me.

## Current version 1.5