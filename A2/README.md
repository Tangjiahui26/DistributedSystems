# CPEN533_A2

## A2: Group Membership

### Usage

We built our system using Python, so as long as the VM nodes have `Python3` environment, the user can simply run our program using commands like `python3 daemon.py`.

After entering the daemon process, the user needs to let the introducer node join the group first. This operation can be done by entering 'join' into the terminal. If a node wants to leave the group, it can enter 'leave' to the terminal. We also support some other command operations, like 'ml' will print the membership list, and 'id' will print the random id of the node.

In addition, we create a shell file called `run.sh` to help start our program. The user can easily run our program by using `./run.sh`.


### Code and Report

More details of our system can be found here:
- Source Code (daemon.py)
  + [daemon.py](https://github.com/lpalazzi/CPEN533_assignments/blob/master/A2/daemon.py)
  + [run.sh](https://github.com/lpalazzi/CPEN533_assignments/blob/master/A2/run.sh)

- Measurements
  + [Measurements Result and Plotting](https://github.com/lpalazzi/CPEN533_assignments/tree/master/A2/measurements)
  
- Report
  + [CPEN_533_A2.pdf](https://github.com/lpalazzi/CPEN533_assignments/blob/master/A2/Report/CPEN_533_A2.pdf)
  
