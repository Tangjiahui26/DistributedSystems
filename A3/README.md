# CPEN533_A3

## A3: fs533

The goal of this programming assignment is to build a simple distributed file system that we will call fs533.

### Usage

Similar to assignment 2, we built our fs533 file system using Python, so if the VM node has `Python3` environment, then user can simply run our program using commands like `python3 fs533.py`.

After entering the file system, since we reused our group membership code in assignment 2, so the user should let the introducer node join the file system first (input 'join' into the terminal). 

Then the user can follow our command lists to conduct operations on the file system:

```
        ===== Command Lists =====
        ---> join: Join the group.
        ---> leave: Leave the group.
        ---> ml: Print membership List
        ---> id: Print current id of the server
        ---> put [localfilename] [fs533filename]: add a local file to fs533 with the given fs533 name
        ---> get [fs533filename] [localfilename]:  fetch a fs533 file to the local machine
        ---> remove [fs533filename] : delete a file from fs533
        ---> ls : list all files in fs533
        ---> locate [fs533filename] : list all machines (name / id / IP address) of the servers that contain a copy of the file
        ---> lshere : list all fs533 files stored on the local machine
        ---> test : test the basic operations of fs533 file system
 ```

 ### Code and Report

 More details can be found here:
 - Source Code
 + [fs533.py](https://github.com/CPEN5AB/a2-summer-2019-team-3/blob/master/A3/fs533.py)
 + [daemon.py](https://github.com/CPEN5AB/a2-summer-2019-team-3/blob/master/A3/daemon.py)

 - Measurements
 + [Measurements and Plotting](https://github.com/CPEN5AB/a2-summer-2019-team-3/tree/master/A3/Measurements)

 - Report
 + [CPEN_533_A3.pdf](https://github.com/CPEN5AB/a2-summer-2019-team-3/blob/master/A3/Report/CPEN_533_A3.pdf)
