# DistributedSystems

## A1: Distributed Log Querying

### Requirement

For this assignment, we are using the free-tier of Amazon's cloud services to create EC2 instances (VMs) so that we can create our own small distributed system.

This program allows us to query distributed log files on multiple machines, from any one of those machines. Also, our program is fault-tolerant, i.e. it will fetch answers from all machines that have not failed. 

- Source Code: [Assignment1](https://github.com/Tangjiahui26/DistributedSystems/tree/master/A1)
- Report: [CPEN_533_A1.pdf](https://github.com/Tangjiahui26/DistributedSystems/blob/master/A1/Report/CPEN_533_A1.pdf)

## A2: Group Membership

### Requirement

In this assignment, we build the basis for a group communication system: a membership service. The membership list will update itself when: a new machine joins the group; a machine leaves the group voluntarily; a machine fails. Our program is able to avoid at least three machine failures simultaneously. 

- Source Code: [Assignment2](https://github.com/Tangjiahui26/DistributedSystems/tree/master/A2)
- Source Code (C++ Version): [A2-C++](https://github.com/Tangjiahui26/DistributedSystems/tree/master/A2_C%2B%2B/GroupMembership)
- Report: [CPEN_533_A2.pdf](https://github.com/Tangjiahui26/DistributedSystems/blob/master/A2/Report/CPEN_533_A2.pdf)

## A3: fs533

### Requirement

The goal for this assignment is to build a simple distributed file system called fs533. This file system is a simplification of the Hadoop Distributed File System (HDFS). Our file system is able to tolerate two server/machine failures at a time.

- Source Code: [Assignment3](https://github.com/Tangjiahui26/DistributedSystems/tree/master/A3)
- Report: [CPEN_533_A3.pdf](https://github.com/Tangjiahui26/DistributedSystems/blob/master/A3/Report/CPEN_533_A3.pdf)
