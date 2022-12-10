# Infrastructures for Cloud Computing Project [Teacher Boris Teabe]
## Table of contents
- [Introduction](#1-introduction)
- [Installation and Usage](#2-installation-and-usage)
- [Problems](#3-problems)


## 1. Introduction
- This project takes place in your class on infrastructures for Cloud computing and the results with be counted as a percentage of your final evaluation at the end of the semester.
- You have to automate the deployment of Kubernetes on a cluster of virtual
machines allocated on Amazon AWS.
- The Goal of the project will be to implement scripts that will allow to deploy autimatically Kubernetes on a cluster built in AWS EC2.

## 2. Installation and Usage
- For running, you must create aws account and create a pem key for paramiko ssh access
- [user], [access key ID] and [Secret access key] are required for boto3
- To run the project, please run file by the number indexed


## 3. Problems

### 3.1. CPUs & Memmory requirement
At first, while starting the project, because we dont read the document carefully so we dont know about the system requirement of Kubernetes. 
```
2 GB or more of RAM per machine (any less will leave little room for your apps).
2 CPUs or more.
```
So when using ec2 t2.micro, the kubernetes can not run normally. We must change it to t2.medium

### 3.2. Automate deployment
There are lot of bug in this step. It took so much time of us to research and solve problem. 

### 3.3. Authenticate problem
We did meet an authenticate problem when trying to create instance. We cant define the reason but then we try to re-create new user. The problem has been solved

### 3.3. Limited instance number
```
 An error occurred (VcpuLimitExceeded) when calling the RunInstances operation: You have requested more vCPU capacity than your current vCPU limit of 32 allows for the instance bucket that the specified instance type belongs to. Please visit http://aws.amazon.com/contact-us/ec2-request to request an adjustment to this limit.
 ```
 With this problem, we need to terminate instances

