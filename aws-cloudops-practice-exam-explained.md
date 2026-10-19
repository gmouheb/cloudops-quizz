# AWS CloudOps Engineer Practice Assessment: Questions and Explained Answers

65 questions from the AWS Skill Builder official practice exam (AWS Certified CloudOps Engineer - Associate, SOA-C03), each with its answer options, the suggested answer, why it is correct, and why the other options are incorrect.

The attempt's summary page reported 65 of 65 correct (score 1000, passing score 720). The explanations are my own reasoning, not AWS's official rationale.

## Answer key

| # | Answer | Topic |
|---|---|---|
| 1 | C | ALB subnet for a new Availability Zone |
| 2 | D, E | HTTPS unreachable behind an ALB |
| 3 | B | Containers with least overhead (ECS) |
| 4 | B | AWS WAF rate-based rule |
| 5 | D | `iam:PermissionsBoundary` condition key |
| 6 | C | Alarm when all ALB targets are unhealthy |
| 7 | C | Scheduled Lambda invocation |
| 8 | C | SSH connection failure |
| 9 | D | CloudWatch agent in an Auto Scaling group |
| 10 | A | CloudFormation S3 bucket, random name, encrypted |
| 11 | A | AWS Budgets per team |
| 12 | B | VPC out of IP addresses |
| 13 | A | Lambda Insights debug logging |
| 14 | D | Keep RDS after stack deletion |
| 15 | A | Incomplete multipart uploads |
| 16 | B | CloudWatch agent not publishing logs |
| 17 | A | Email on EC2 state change |
| 18 | D | Private subnet access to S3 |
| 19 | C | EKS anomalies with recommendations |
| 20 | D | CloudFront restricted content |
| 21 | B | Lambda reserved concurrency |
| 22 | B | Data Lifecycle Manager retention |
| 23 | C | Disaster recovery with minimum RTO |
| 24 | C | SQL injection protection |
| 25 | B | VPC Flow Logs: ACCEPT in, REJECT out |
| 26 | C | 500 GB upload failures |
| 27 | B, D | Consistent CloudWatch agent configuration |
| 28 | C | S3 Cross-Region Replication defaults |
| 29 | D | CloudWatch agent on EKS |
| 30 | C, E | Lowest latency between instances |
| 31 | D | CloudWatch Logs agent, no logs |
| 32 | B | Re-enable CloudTrail without code |
| 33 | C | Users repeatedly prompted to log in |
| 34 | B | 1-minute EC2 metrics |
| 35 | C | RDS availability |
| 36 | D | `InstanceLimitExceeded` |
| 37 | B | Cross-account role for AWS services |
| 38 | C | Encrypt an existing RDS instance |
| 39 | C | EBS restore latency |
| 40 | D, E | Elastic Beanstalk full capacity deployments |
| 41 | C | Predictable daily traffic |
| 42 | C | Analyze instances before termination |
| 43 | A | 70/30 traffic split with failover |
| 44 | D | EventBridge API destination errors |
| 45 | B | DynamoDB read latency |
| 46 | B | Terminate instances from unapproved AMIs |
| 47 | A | Fixed fleet of 10 instances |
| 48 | A | Multi-Region automatic failover |
| 49 | B | Run a script with SSH blocked |
| 50 | C | Dedicated, customer-controlled HSMs |
| 51 | A, E | Presigned URL stopped working |
| 52 | D | Share a transit gateway across accounts |
| 53 | C | Route by location of resources |
| 54 | A, C | CloudFormation `DELETE_FAILED` |
| 55 | B | Automated patching |
| 56 | A | EventBridge rules for many Lambda functions |
| 57 | A | ALB health check configuration |
| 58 | B | S3 Object Lock for 10 years |
| 59 | B | Bucket policy IP restriction |
| 60 | A | Centralized alarms across an organization |
| 61 | D | EventBridge rule does not invoke Lambda |
| 62 | B | On-premises to S3 without the internet |
| 63 | C | Daily EC2 backups |
| 64 | C | Shared file system across Availability Zones |
| 65 | A, E | ElastiCache (Memcached) high CPU |

---

## Question 1

An ecommerce website runs on Amazon EC2 instances in an Auto Scaling group behind an Application Load Balancer (ALB). A CloudOps engineer is extending the Auto Scaling group to span one more Availability Zone. EC2 instances in the new Availability Zone are in the running state but fail to register with the target group.

How can the CloudOps engineer resolve this issue?

- A. Attach the Availability Zone to the target group.
- B. Update inbound rules on the security groups of the EC2 instances.
- C. Attach at least one subnet in the new Availability Zone to the ALB.
- D. Update outbound rules on the security groups of the ALB.

**Answer: C**

**Why correct:** An ALB only routes to targets in Availability Zones that are enabled on the load balancer, and a zone is enabled by attaching one of its subnets to the ALB. Instances in a zone that is not enabled cannot be used as targets even though they are running.

**Why the others are incorrect:**

- **A:** Target groups have no Availability Zone attachment; zones are enabled on the load balancer.
- **B:** A bad inbound rule would show targets as unhealthy, not block registration, and the existing zones work with the same security group.
- **D:** ALB outbound rules would cause health check failures in all zones, not only the new one.

---

## Question 2

A company is preparing to launch a new website. The website runs on Amazon EC2 instances behind an Application Load Balancer (ALB). The company launched the instances by using a custom Amazon Machine Image (AMI) from an EC2 instance that runs without problems in a different VPC in the same AWS Region.

After deployment of the new EC2 instances, external testing failed to connect to the website by using HTTPS. The website is reachable by using SSH through a bastion host instance that runs in the same VPC.

Which combination of steps should a CloudOps engineer take to find the problem? (Select TWO)

- A. Ensure that both the system status and instance reachability checks for the instances are succeeding.
- B. Ensure that the instances are located in a subnet with 0.0.0.0/0 access routed to an internet gateway.
- C. Ensure that the instances have a public IP address or an Elastic IP address that is assigned to each instance's elastic network interface.
- D. Ensure that the security group that is assigned to the instances is open to port 443 from the ALB's security group.
- E. Ensure that the ALB is assigned to a subnet with 0.0.0.0/0 routed to an internet gateway.

**Answer: D, E**

**Why correct:**

- **D:** The instances must allow inbound 443 from the ALB's security group. Security groups are VPC-scoped, so the new instances have a different group whose rules may not include 443. SSH working through the bastion only proves port 22 is open.
- **E:** An internet-facing ALB must sit in public subnets, meaning subnets with a 0.0.0.0/0 route to an internet gateway. Without that, external clients cannot reach the ALB.

**Why the others are incorrect:**

- **A:** SSH through the bastion succeeds, so the instances are running and reachable.
- **B:** Instances behind an ALB do not need to be in public subnets; the ALB reaches them over private IPs.
- **C:** For the same reason, the instances do not need public or Elastic IP addresses.

---

## Question 3

A CloudOps engineer needs to deploy a containerized web application across multiple Availability Zones. The container images are stored in Amazon ECR.

Which deployment method will meet these requirements with the LEAST operational overhead?

- A. Use AWS Step Functions to orchestrate container deployments to Amazon EC2 instances across multiple Availability Zones.
- B. Use Amazon ECS with service auto scaling across multiple Availability Zones and an Application Load Balancer (ALB).
- C. Use AWS CloudFormation templates to deploy containers to Amazon EC2 instances across multiple Availability Zones.
- D. Use AWS Systems Manager Run Command to deploy the containers to an Auto Scaling group of Amazon EC2 instances across multiple Availability Zones.

**Answer: B**

**Why correct:** ECS is the managed container orchestrator and pulls images from ECR natively. An ECS service spreads tasks across Availability Zones, replaces failed tasks, scales automatically, and registers tasks with the ALB, so there is no custom deployment logic to maintain.

**Why the others are incorrect:**

- **A:** Step Functions is a workflow orchestrator, not a container scheduler; placement, health, and rollout logic would be custom.
- **C:** CloudFormation can provision the instances, but running containers on them still means managing the runtime, scheduling, and restarts.
- **D:** Run Command executes ad hoc commands; it gives no service scheduling, health replacement, or load balancer integration.

---

## Question 4

A CloudOps engineer needs to block malicious traffic that is reaching a company's web servers. The malicious traffic is distributed over many IP addresses. The malicious traffic consists of a significantly higher number of connections than the company typically receives from legitimate users. The CloudOps engineer needs to protect the web servers.

Which solution meets these requirements with the LEAST operational overhead?

- A. Set the network ACL for the subnet that is assigned to the web servers. Add deny rules for malicious sources.
- B. Place the web servers behind AWS WAF. Establish the rate limit to create a denylist.
- C. Create a security group for the web servers. Add deny rules for malicious sources.
- D. Use Amazon CloudFront to cache all pages and remove the traffic from the web servers.

**Answer: B**

**Why correct:** A WAF rate-based rule automatically blocks any source IP that exceeds a request threshold and unblocks it when the rate drops. That fits traffic spread over many IPs with abnormally high connection counts, and it needs no manual list maintenance.

**Why the others are incorrect:**

- **A:** Network ACL deny rules must be added by hand per source, and the rule limit per ACL is too low for a widely distributed attack.
- **C:** Security groups support only allow rules; they cannot deny.
- **D:** Caching reduces origin load but blocks nothing, and uncacheable requests still reach the web servers.

---

## Question 5

A company wants to enhance its security by applying IAM permissions boundaries. The company tries to use IAM policy conditions and receives the following error:

"Error: error updating IAM Role (role-name) assume role policy: AccessDenied: User: id-arn is not authorized to perform: iam:UpdateAssumeRolePolicy on resource: role role-name status code: 403, request id: request-id"

The policy that contains the condition includes the following snippet:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CreateOrChangeOnlyWithBoundary",
            "Effect": "Allow",
            "Action": "UpdateAssumeRolePolicy",
            "Resource": "arn:aws:iam::123456789012:role/role-name",
            "Condition": {
                "StringEquals": {
                    "iam:PermissionsBoundary": "arn:aws:iam::123456789012:policy/MyBoundaryPolicy"
                }
            }
        }
    ]
}
```

What is the reason for the error?

- A. Permissions boundaries are not allowed with IAM policies.
- B. IAM user id-arn is not allowed to assume role-name.
- C. Condition keys are not allowed in conjunction with permissions boundaries.
- D. The UpdateAssumeRolePolicy action is not compatible with the iam:PermissionsBoundary condition key.

**Answer: D**

**Why correct:** The `iam:PermissionsBoundary` condition key is only evaluated for a specific set of IAM actions: `CreateUser`, `CreateRole`, the put/delete permissions boundary actions, and the attach/detach/put/delete policy actions for users and roles. `iam:UpdateAssumeRolePolicy` is not one of them, so the key is absent from the request context, the `StringEquals` condition never matches, and the Allow does not apply. The result is an implicit deny and the 403.

**Why the others are incorrect:**

- **A:** Permissions boundaries are themselves IAM managed policies and work alongside identity policies.
- **B:** The error is about `iam:UpdateAssumeRolePolicy` (editing the role's trust policy), not `sts:AssumeRole`.
- **C:** Condition keys are valid with permissions boundaries; `iam:PermissionsBoundary` exists for exactly that purpose.

---

## Question 6

A CloudOps engineer is managing a web application that runs on Amazon EC2 instances behind an Application Load Balancer (ALB). The instances run in an EC2 Auto Scaling group. The CloudOps engineer wants to set an alarm for when all target instances associated with the ALB are unhealthy.

Which condition should be used with the alarm?

- A. AWS/EC2 StatusCheckFailed <= 0
- B. AWS/ApplicationELB UnhealthyHostCount >= 1
- C. AWS/ApplicationELB HealthyHostCount <= 0
- D. AWS/EC2 StatusCheckFailed >= 1

**Answer: C**

**Why correct:** All targets are unhealthy exactly when the number of healthy targets is zero, so `HealthyHostCount <= 0` matches the requirement regardless of how many instances the Auto Scaling group is running.

**Why the others are incorrect:**

- **B:** `UnhealthyHostCount >= 1` fires when any single target is unhealthy, not when all are.
- **A and D:** `StatusCheckFailed` is a per-instance EC2 metric for system and instance status checks. It does not reflect ALB target health, and an instance can pass EC2 status checks while failing the ALB health check.

---

## Question 7

A CloudOps engineer needs to automate the invocation of an AWS Lambda function. The Lambda function must run at the end of each day to generate a report on data that is stored in an Amazon S3 bucket.

What is the MOST operationally efficient solution that meets these requirements?

- A. Deploy an Amazon EC2 instance with a cron job to invoke the Lambda function.
- B. Create an Amazon EventBridge rule that has an event pattern for Amazon S3 and the Lambda function as a target.
- C. Create an Amazon EventBridge rule that has a schedule and the Lambda function as a target.
- D. Create an S3 event notification to invoke the Lambda function whenever objects change in the S3 bucket.

**Answer: C**

**Why correct:** The requirement is time-based (end of each day), so a scheduled EventBridge rule with a cron expression invokes the function directly, with no infrastructure to manage.

**Why the others are incorrect:**

- **A:** An EC2 instance running cron adds a server to patch, monitor, and pay for, and it is a single point of failure.
- **B:** An S3 event pattern triggers on bucket activity, not on a daily schedule.
- **D:** S3 event notifications invoke the function on every object change, not once a day.

---

## Question 8

A company is hosting backend web services across Amazon EC2 Linux instances in public subnets in a VPC. A CloudOps engineer tries to connect to the instance by using SSH but is unable to connect.

What could be the cause of the failed connection?

- A. The security group does not allow outbound traffic on port 3389.
- B. The network ACL does not allow outbound traffic on port 80.
- C. The security group does not allow inbound traffic on port 22.
- D. The network ACL does not allow inbound traffic on port 443.

**Answer: C**

**Why correct:** SSH uses TCP port 22, and security groups deny all inbound traffic that is not explicitly allowed, so a missing inbound rule for port 22 blocks the connection.

**Why the others are incorrect:**

- **A:** Port 3389 is RDP for Windows, and security groups are stateful, so outbound rules do not affect replies to an inbound SSH session.
- **B:** Port 80 is HTTP and has nothing to do with SSH.
- **D:** Port 443 is HTTPS; a network ACL would need to block inbound port 22 or the outbound ephemeral ports to break SSH.

---

## Question 9

A company has a web application that runs on Amazon EC2 instances in an Auto Scaling group. The company stores the application logs in the /var/log/application directory on each instance. A CloudOps engineer must configure an automated solution to send logs to Amazon CloudWatch Logs.

Which solution will meet this requirement with the LEAST operational overhead?

- A. Enable instance-level logging for the Auto Scaling group. Configure instance-level logging to send application logs to CloudWatch Logs.
- B. Create an AWS Config rule to check for logs in the /var/log/application directory on the EC2 instances. Configure the rule to provide remediation by sending the logs to CloudWatch Logs.
- C. Create an AWS Lambda function that is invoked by EC2 instance launch events. Configure the function to copy logs from the /var/log/application directory to CloudWatch Logs.
- D. Configure user data scripts to install the Amazon CloudWatch agent. Create a CloudWatch agent configuration file to monitor the /var/log/application directory.

**Answer: D**

**Why correct:** The CloudWatch agent is the supported way to stream log files from an instance's file system to CloudWatch Logs. Putting the install and configuration in the launch template's user data means every instance the Auto Scaling group launches ships its logs automatically.

**Why the others are incorrect:**

- **A:** Auto Scaling groups have no "instance-level logging" feature that forwards application log files.
- **B:** AWS Config evaluates resource configuration; it cannot read files on an instance or ship log contents.
- **C:** A Lambda function invoked at launch cannot read the instance's file system, and a one-time invocation would not stream logs continuously.

---

## Question 10

A CloudOps engineer needs to create an Amazon S3 bucket as a resource in an AWS CloudFormation template. The bucket name must be randomly generated, and the bucket must be encrypted. Other resources in the template will reference the bucket.

Which CloudFormation resource definition should the CloudOps engineer use to meet these requirements?

**A.**

```yaml
Bucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketEncryption:
      ServerSideEncryptionConfiguration:
        - ServerSideEncryptionByDefault:
            SSEAlgorithm: AES256
```

**B.**

```yaml
Bucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: "DOC-EXAMPLE-BUCKET"
```

**C.**

```yaml
Bucket:
  Type: AWS::S3::Bucket
  Properties:
```

**D.**

```yaml
Bucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: "DOC-EXAMPLE-BUCKET"
    BucketEncryption:
      ServerSideEncryptionConfiguration:
        - ServerSideEncryptionByDefault:
            SSEAlgorithm: AES256
```

**Answer: A**

**Why correct:** Omitting `BucketName` makes CloudFormation generate a unique name from the stack name, logical ID, and a random suffix. `BucketEncryption` sets default SSE-S3 encryption, and other resources can reference the bucket with `!Ref Bucket` or `!GetAtt Bucket.Arn`.

**Why the others are incorrect:**

- **B:** It hardcodes the bucket name and has no encryption configuration.
- **C:** The name is generated, but no encryption is defined in the template.
- **D:** Encryption is set, but the name is hardcoded instead of randomly generated.

---

## Question 11

A company needs to ensure strict adherence to a budget for 25 applications deployed on AWS. Separate teams are responsible for storage, compute, and database costs. A CloudOps engineer must implement an automated solution to alert each team when their projected spend will exceed a quarterly amount that has been set by the finance department. The solution cannot incur additional compute, storage, or database costs.

Which solution will meet these requirements?

- A. Use AWS Budgets to create a cost budget for each team, filtering by the services they own. Specify the budget amount defined by the finance department along with a forecasted cost threshold. Enter the appropriate email recipients for each budget.
- B. Configure AWS Cost and Usage Reports to send a daily report to an Amazon S3 bucket. Create an AWS Lambda function that will evaluate spend by service and notify each team by using Amazon SNS notifications. Invoke the Lambda function when a report is placed in the S3 bucket.
- C. Configure AWS Cost and Usage Reports to send a daily report to an Amazon S3 bucket. Create a rule in Amazon EventBridge to evaluate the spend by service and notify each team by using Amazon SQS when the cost threshold is exceeded.
- D. Use AWS Budgets to create one cost budget and select each of the services in use. Specify the budget amount defined by the finance department along with the forecasted cost threshold. Enter the appropriate email recipients for the budget.

**Answer: A**

**Why correct:** AWS Budgets supports quarterly cost budgets, service filters, and alerts on forecasted spend, so each team gets its own alert when its projected cost will exceed the finance department's amount. It needs no compute, storage, or database resources.

**Why the others are incorrect:**

- **B:** It stores reports in S3 and runs Lambda, which adds storage and compute costs, and it requires custom code.
- **C:** It also incurs S3 storage costs, EventBridge rules cannot evaluate report contents, and SQS is a queue, not a notification service for teams.
- **D:** A single budget covering all services alerts on combined spend, so it cannot tell each team when its own projected spend exceeds its limit.

---

## Question 12

A company has a VPC with a private IP address space of 10.0.0.0/16. The company has used all of the existing private IP space.

Which solution will resolve this issue with the LEAST operational overhead?

- A. Change the private IP address space from 10.0.0.0/16 to 10.0.0.0/8.
- B. Find an unused CIDR block of private IP addresses. Add the CIDR block to the VPC.
- C. Set up a new VPC with a new private address space. Establish VPC peering between the two VPCs.
- D. Convert the IP addresses to IPv6.

**Answer: B**

**Why correct:** A VPC supports secondary IPv4 CIDR blocks, so an additional non-overlapping block can be associated with the existing VPC and new subnets created from it. Nothing is rebuilt or migrated, and routing between the blocks inside the VPC is automatic.

**Why the others are incorrect:**

- **A:** A VPC's primary CIDR block cannot be modified after creation, and the largest block a VPC allows is /16, so /8 is invalid.
- **C:** A new VPC with peering works but adds route tables, security group changes, and a second VPC to manage.
- **D:** A VPC cannot simply be converted to IPv6; adopting it requires reconfiguring subnets, routes, security rules, and applications.

---

## Question 13

An AWS Lambda function that uses a Python runtime is having performance issues. A CloudOps engineer needs to enable debug logging on the Lambda Insights extension.

Which solution will meet this requirement?

- A. Set the following environment variable on the Lambda function: LAMBDA_INSIGHTS_LOG_LEVEL=info.
- B. Use the following command in the first line of the Python code to configure monitoring: DETAILED_MONITORING=true.
- C. Pass the LAMBDA_INSIGHTS=true parameter as the first parameter of the Lambda function.
- D. Enable the Python debugger in the first line of the Lambda function by using pdb.set_trace().

**Answer: A**

**Why correct:** The Lambda Insights extension reads its logging level from the `LAMBDA_INSIGHTS_LOG_LEVEL` environment variable, and setting it to `info` turns on the extension's debug logging, written to the function's CloudWatch Logs log group. It is a configuration change only.

**Why the others are incorrect:**

- **B:** `DETAILED_MONITORING=true` is not a valid Python statement or a Lambda Insights setting.
- **C:** Lambda Insights is not controlled by a parameter passed to the function handler.
- **D:** `pdb.set_trace()` starts an interactive debugger, which cannot be used in Lambda's non-interactive environment and is unrelated to the extension's logging.

---

## Question 14

A CloudOps engineer manages an AWS CloudFormation template that provisions Amazon EC2 instances, an Application Load Balancer, and Amazon RDS instances. As part of an ongoing transformation project, CloudFormation stacks are being created and deleted continuously. The CloudOps engineer needs to ensure that the RDS instances continue running after a stack has been deleted.

Which action should be taken to meet these requirements?

- A. Enable termination protection on the stack.
- B. Set the deletion-protection parameter on RDS resources.
- C. Edit the template to remove the RDS resources and update the stack.
- D. Set the DeletionPolicy attribute for RDS resources to Retain in the template.

**Answer: D**

**Why correct:** With `DeletionPolicy: Retain`, CloudFormation leaves the RDS instances running and removes them from its management when the stack is deleted. The stack deletion completes cleanly and the rest of the resources are removed.

**Why the others are incorrect:**

- **A:** Termination protection blocks deletion of the whole stack, which conflicts with stacks being deleted continuously.
- **B:** RDS deletion protection keeps the instance, but CloudFormation's delete call fails, leaving the stack in `DELETE_FAILED`.
- **C:** Removing the RDS resources from the template and updating the stack deletes those instances.

---

## Question 15

A CloudOps engineer manages a company's Amazon S3 buckets. The CloudOps engineer has identified 5 GB of incomplete multipart uploads in an S3 bucket in the company's AWS account. The CloudOps engineer needs to reduce the number of incomplete multipart upload objects in the S3 bucket.

Which solution will meet this requirement?

- A. Create an S3 Lifecycle rule on the S3 bucket to delete expired markers or incomplete multipart uploads.
- B. Enable S3 Versioning on the S3 bucket that contains the incomplete multipart uploads.
- C. Require users that perform uploads of files into Amazon S3 to use the S3 TransferUtility.
- D. Enable S3 Intelligent-Tiering to automatically clean up incomplete multipart uploads.

**Answer: A**

**Why correct:** A lifecycle rule with the `AbortIncompleteMultipartUpload` action automatically aborts uploads that have not completed within a set number of days after initiation and deletes their stored parts. That removes the existing 5 GB and keeps new incomplete uploads from accumulating.

**Why the others are incorrect:**

- **B:** Versioning keeps multiple versions of completed objects; it does nothing to incomplete upload parts.
- **C:** TransferUtility is an SDK upload helper; it does not clean up parts already in the bucket.
- **D:** Intelligent-Tiering moves completed objects between access tiers; it does not remove incomplete multipart uploads.

---

## Question 16

A company has a policy that all Amazon EC2 instance logs must be published to Amazon CloudWatch Logs. A CloudOps engineer is troubleshooting an EC2 instance that is running Amazon Linux 2. The EC2 instance is not publishing logs to CloudWatch Logs. The Amazon CloudWatch agent is running on the EC2 instance, and the agent configuration file is correct.

What should the CloudOps engineer do to resolve the issue?

- A. Inspect the retention period of the CloudWatch Logs log group. Ensure that the retention period is set to a value that is greater than 1 day.
- B. Ensure that the IAM role that is attached to the EC2 instance has permissions in CloudWatch Logs for the CreateLogGroup, CreateLogStream, PutLogEvents, and DescribeLogStreams actions.
- C. Configure the AWS CLI on the EC2 instance. Create a cron job that calls the PutLogEvents API operation to push the log files to CloudWatch every 5 minutes.
- D. Set up an Amazon Kinesis data stream that is running in the same AWS Region as the EC2 instance. Configure the CloudWatch agent on the EC2 instance to send CloudWatch events to the data stream.

**Answer: B**

**Why correct:** The agent is running and its configuration is correct, so the remaining cause is authorization. The agent uses the instance profile's role to call the CloudWatch Logs API, and without those permissions its calls are denied. The `CloudWatchAgentServerPolicy` managed policy covers these actions.

**Why the others are incorrect:**

- **A:** Retention controls how long stored log events are kept; it does not affect whether the agent can deliver them.
- **C:** A cron job calling `PutLogEvents` duplicates what the agent does and would fail with the same missing permissions.
- **D:** The agent publishes to CloudWatch Logs directly; a Kinesis data stream is not part of that path.

---

## Question 17

A company has 10 Amazon EC2 instances in its production account. A CloudOps engineer must ensure that email notifications are sent to administrators each time there is an EC2 instance state change.

Which solution will meet this requirement?

- A. Create an Amazon EventBridge rule that publishes a message to an Amazon SNS topic when an EC2 instance state changes. This SNS topic then sends notifications to its email subscribers.
- B. Create an Amazon EventBridge rule that publishes a message to an Amazon SQS queue when an EC2 instance state changes. This SQS queue then sends notifications to its email subscribers.
- C. Configure an Amazon Route 53 simple routing policy that publishes a message to an Amazon SNS topic when an EC2 instance state changes. This SNS topic then sends notifications to its email subscribers.
- D. Configure an Amazon Route 53 simple routing policy that publishes a message to an Amazon SQS queue when an EC2 instance state changes. This SQS queue then sends notifications to its email subscribers.

**Answer: A**

**Why correct:** EC2 emits an "EC2 Instance State-change Notification" event to EventBridge on every state transition. A rule matching that event with an SNS topic as its target delivers an email to each subscribed administrator.

**Why the others are incorrect:**

- **B:** SQS is a queue that consumers poll; it has no email subscribers and cannot send notifications.
- **C:** A Route 53 simple routing policy answers DNS queries; it does not detect EC2 state changes or publish to SNS.
- **D:** It combines both problems: Route 53 cannot detect state changes, and SQS cannot send email.

---

## Question 18

A company is running an application on Amazon EC2 instances that are located in a private subnet. The application requires access to data that is stored in an Amazon S3 bucket.

Which solution meets this requirement with the LEAST operational overhead?

- A. Set up an AWS Direct Connect connection. Create a private virtual interface (VIF) to route traffic to the S3 bucket.
- B. Establish a VPC peering connection between the private subnet and Amazon S3.
- C. Set up and configure an AWS Client VPN connection. Use a prefix list to route traffic over that link.
- D. Create and configure a gateway VPC endpoint to connect to the S3 bucket.

**Answer: D**

**Why correct:** A gateway endpoint for S3 adds a route in the private subnet's route table that sends S3 traffic over the AWS network, so the instances reach the bucket without a NAT gateway, internet gateway, or public IPs. It has no additional charge and nothing to maintain.

S3 supports two endpoint types:

| Type | How it works | Cost | When to use |
|---|---|---|---|
| Gateway endpoint | Adds a route for the S3 prefix list to the subnet's route table | Free | Access from resources inside the VPC |
| Interface endpoint (PrivateLink) | Places a network interface with a private IP in the subnet | Hourly and per-GB charges | Access from on-premises over Direct Connect or VPN, or from another VPC or Region |

**Why the others are incorrect:**

- **A:** Direct Connect links on-premises networks to AWS; it is not a path from instances in a VPC to S3.
- **B:** VPC peering connects two VPCs. S3 is not a VPC, so it cannot be peered.
- **C:** Client VPN gives remote users access into a VPC; it is not a path from EC2 instances to S3.

---

## Question 19

A company is using Amazon CloudWatch alarms to monitor Amazon EKS workloads. The alarms are initiated through a threshold definition and are not helping the EKS cluster operate more efficiently.

A CloudOps engineer must implement a solution that identifies anomalies and generates recommendations for how to address the anomalies.

Which solution will meet these requirements?

- A. Use CloudWatch anomaly detection to identify anomalies and provide recommendations.
- B. Use CloudWatch Container Insights to identify anomalies and provide recommendations.
- C. Use CloudWatch Container Insights with Amazon DevOps Guru to identify anomalies and provide recommendations.
- D. Use CloudWatch anomaly detection with CloudWatch Container Insights to identify anomalies and provide recommendations.

**Answer: C**

**Why correct:** Container Insights collects the EKS cluster, node, and pod metrics. DevOps Guru applies machine learning to those metrics to detect anomalous behavior and produces insights that include recommendations for fixing the cause. It is the only option that covers both detection and recommendations.

**Why the others are incorrect:**

- **A:** CloudWatch anomaly detection builds an expected-value band and can alarm on deviations, but it gives no remediation recommendations.
- **B:** Container Insights collects and visualizes container metrics and logs; on its own it neither detects anomalies with ML nor recommends fixes.
- **D:** Combining the two detects anomalies in container metrics but still produces no recommendations.

---

## Question 20

A CloudOps engineer needs to configure a solution that will deliver digital content to a set of authorized users through Amazon CloudFront. Unauthorized users must be restricted from access.

Which solution will meet these requirements?

- A. Store the digital content in an Amazon S3 bucket that does not have public access blocked. Use signed URLs to access the S3 bucket through CloudFront.
- B. Store the digital content in an Amazon S3 bucket that has public access blocked. Use an origin access control (OAC) to deliver the content through CloudFront. Enable field-level encryption.
- C. Store the digital content in an Amazon S3 bucket that does not have public access blocked. Use signed cookies for restricted delivery of the content through CloudFront.
- D. Store the digital content in an Amazon S3 bucket that has public access blocked. Use an origin access control (OAC) to deliver the content through CloudFront. Restrict S3 bucket access with signed URLs in CloudFront.

**Answer: D**

**Why correct:** Two controls are needed, and D has both. OAC with public access blocked means only CloudFront can read the bucket, so users cannot bypass CloudFront with a direct S3 URL. Signed URLs mean CloudFront serves content only to users who hold a valid signed URL.

**Why the others are incorrect:**

- **A and C:** The bucket is not blocked from public access, so unauthorized users can fetch objects directly from S3 and skip the signed URL or cookie check.
- **B:** The origin is locked down, but nothing restricts viewers. Field-level encryption protects sensitive fields in POST data sent to the origin; it is not viewer access control.

---

## Question 21

A company runs an image-processing application by using AWS Lambda. Each processing job runs in a single Lambda invocation. A CloudOps engineer needs to ensure that there is enough capacity to run 500 simultaneous jobs, even when other Lambda functions run for other applications. The CloudOps engineer has already increased service limits within the AWS Region.

Which setting configuration will meet this requirement?

- A. Modify the memory settings on the image-processing Lambda function to allow for 500 parallel runs.
- B. Set the reserved concurrency for the image-processing Lambda function to 500.
- C. Modify the maximum concurrency limit for the image-processing Lambda function to 500.
- D. Set the provisioned concurrency for the image-processing Lambda function to 500.

**Answer: B**

**Why correct:** Reserved concurrency sets aside part of the account's Regional concurrency for one function. With 500 reserved, other functions cannot consume that capacity, so the function can always run 500 simultaneous invocations. It has no additional charge.

**Why the others are incorrect:**

- **A:** Memory controls the resources of each execution environment, not how many invocations can run at once.
- **C:** A maximum concurrency setting caps how many invocations an event source sends to the function; it limits the function and does not guarantee capacity against other functions.
- **D:** Provisioned concurrency pre-initializes execution environments to remove cold starts and is billed while enabled. The requirement is guaranteed capacity, not lower latency.

---

## Question 22

A company needs to automatically delete Amazon EBS snapshots that are older than 30 days by using Amazon Data Lifecycle Manager.

Which solution will meet this requirement?

- A. Verify that the Amazon S3 Lifecycle policy is selected with a 30-day retention rule.
- B. Create a lifecycle policy in Amazon Data Lifecycle Manager. Set the retention period to 30 days.
- C. Enable snapshot archiving in Amazon Data Lifecycle Manager. Configure a 30-day retention rule for active snapshots.
- D. Create an AWS Lambda function that Amazon Data Lifecycle Manager can call to send a notification when snapshots reach the 30-day threshold.

**Answer: B**

**Why correct:** A Data Lifecycle Manager snapshot policy has a schedule with an age-based retention rule. Setting that rule to 30 days makes the policy delete the snapshots it created once they are older than 30 days, with no code. It only manages snapshots created by the policy.

**Why the others are incorrect:**

- **A:** S3 Lifecycle policies manage objects in S3 buckets; they cannot manage EBS snapshots.
- **C:** Archiving moves snapshots to the lower-cost archive tier, which keeps them instead of deleting them.
- **D:** A notification at the 30-day mark deletes nothing, and Data Lifecycle Manager does not call Lambda functions as part of retention.

---

## Question 23

A company needs to configure a disaster recovery solution for a critical application that runs on AWS.

The company must replicate its Amazon EC2 instances to a secondary AWS Region. The EC2 instances run Amazon Linux 2023.

Which solution will meet these requirements with the MINIMUM recovery time objective (RTO)?

- A. Configure Amazon Data Lifecycle Manager to back up the EC2 instances to a secondary Region. Use Amazon Route 53 for DNS failover to the secondary Region when needed.
- B. Create Amazon Machine Images (AMIs) of all the EC2 instances. Copy the AMIs to the secondary Region. When needed, launch EC2 instances from the AMIs. Use Amazon Route 53 for DNS failover.
- C. Implement AWS Elastic Disaster Recovery to back up the EC2 instances to a secondary Region and to perform failover to the secondary Region when needed.
- D. Configure AWS Backup to back up the EC2 instances to a secondary Region. Use Amazon Route 53 for DNS failover to the secondary Region when needed.

**Answer: C**

**Why correct:** Elastic Disaster Recovery continuously replicates the instances' block storage to a low-cost staging area in the secondary Region. On failover it launches fully provisioned recovery instances from the latest state, giving an RTO of minutes and an RPO of seconds.

**Why the others are incorrect:**

- **A:** Data Lifecycle Manager copies scheduled snapshots or AMIs. Recovery means restoring from the last scheduled copy, which takes longer, and data since that copy is lost.
- **B:** Copying AMIs is backup-and-restore with manual launch steps, so the RTO is longer and the AMIs go stale between copies.
- **D:** AWS Backup also restores from scheduled recovery points, which is slower than launching from continuously replicated data.

---

## Question 24

A company that hosts a multi-tier ecommerce web application on AWS has been alerted to suspicious application traffic. The architecture consists of Amazon EC2 instances deployed across multiple Availability Zones behind an Application Load Balancer (ALB). After examining the instance logs, a CloudOps engineer determines that the suspicious traffic is an attempted SQL injection attack.

What should the CloudOps engineer do to prevent similar attacks?

- A. Enable Amazon GuardDuty. Use Amazon EventBridge to invoke an AWS Lambda function every time GuardDuty detects SQL injection.
- B. Install Amazon Inspector on the EC2 instances, and configure a rules package. Use the findings reports to identify and block SQL injection attacks.
- C. Create an AWS WAF web ACL, and configure a SQL injection rule to add to the web ACL. Associate the AWS WAF web ACL with the ALB.
- D. Create an Amazon CloudFront distribution with the ALB as the origin. Enable AWS Shield Advanced to protect from SQL injection attacks at edge locations.

**Answer: C**

**Why correct:** AWS WAF inspects HTTP(S) requests at layer 7 and has SQL injection match rules (and a managed SQL database rule group) that block malicious requests before they reach the instances. A web ACL can be associated directly with an ALB.

**Why the others are incorrect:**

- **A:** GuardDuty analyzes CloudTrail, VPC Flow Logs, and DNS logs; it does not inspect HTTP request content, and it detects instead of blocking.
- **B:** Amazon Inspector scans for software vulnerabilities and unintended network exposure; it does not filter incoming requests.
- **D:** Shield Advanced protects against DDoS attacks, not SQL injection, which needs WAF rules.

---

## Question 25

A VPC is connected to a company data center by a VPN. An Amazon EC2 instance with the IP address 172.31.16.139 is within a private subnet of the VPC. A CloudOps engineer issued a ping command to the EC2 instance from an on-premises computer with the IP address 203.0.113.12 and did not receive an acknowledgment. VPC Flow Logs were enabled and showed the following:

```
2 123456789010 eni-1235b8ca 203.0.113.12 172.31.16.139 0 0 1 4 336 1432917027 1432917142 ACCEPT OK
2 123456789010 eni-1235b8ca 172.31.16.139 203.0.113.12 0 0 1 4 336 1432917094 1432917142 REJECT OK
```

Which action will resolve the issue?

- A. Modify the VPC network ACL rules to allow inbound traffic from the on-premises computer.
- B. Modify the VPC network ACL rules to allow outbound traffic to the on-premises computer.
- C. Modify the EC2 security group rules to allow outbound traffic to the on-premises computer.
- D. Modify the EC2 security group rules to allow inbound traffic from the on-premises computer.

**Answer: B**

**Why correct:** The inbound ICMP request (203.0.113.12 to 172.31.16.139) was `ACCEPT`, but the reply (172.31.16.139 to 203.0.113.12) was `REJECT`. Security groups are stateful, so a reply to an allowed inbound request is always permitted. Network ACLs are stateless and evaluate the reply against their outbound rules, so the rejection can only come from the network ACL's outbound rules.

**Why the others are incorrect:**

- **A:** The inbound request was accepted, so the inbound rules already allow it.
- **C:** Security groups are stateful; return traffic for an allowed inbound connection is not checked against outbound rules.
- **D:** The `ACCEPT` on the inbound record shows the security group already allows the inbound ping.

---

## Question 26

A company has a data pipeline that collects data hourly and stores the data in Amazon S3. The company has a dataset with a single object that contains 500 GB of time-sensitive data. The upload attempts for the object frequently fail and require complete restarts.

Which solution will improve the upload performance?

- A. Enable Amazon S3 Transfer Acceleration on the S3 bucket.
- B. Configure AWS DataSync to automate transfers of the dataset into Amazon S3.
- C. Configure multipart upload for the dataset.
- D. Enable Amazon S3 Lifecycle policies to transition the dataset after uploading.

**Answer: C**

**Why correct:** Multipart upload splits the object into parts that upload independently and in parallel. A failed part is retried on its own instead of restarting the whole 500 GB transfer, and parallel parts raise throughput. A single PUT is limited to 5 GB, so an object this size requires multipart upload anyway.

**Why the others are incorrect:**

- **A:** Transfer Acceleration speeds up long-distance transfers through edge locations, but a failure still forces a full restart if the upload is not multipart.
- **B:** DataSync automates transfers from storage systems, but it adds an agent and a service to manage and does not address the restart problem as directly.
- **D:** Lifecycle policies act on objects after they are stored; they have no effect on upload performance or reliability.

---

## Question 27

A company's CloudOps engineer manages a fleet of Windows Amazon EC2 instances that run in a single AWS account. The instances have a tag that includes a key of "OS" and a value of "Windows." The company uses AWS Systems Manager to patch the instances.

The company has installed the Amazon CloudWatch agent on the instances, but the configuration is inconsistent. The CloudOps engineer needs to reconfigure every instance to use the same predefined CloudWatch configuration.

Which combination of steps will meet these requirements? (Select TWO)

- A. Create a Systems Manager State Manager association to run the AmazonCloudWatch-ManageAgent Systems Manager Run Command document. Configure the document to use the Amazon S3 bucket location as the configuration source. Target the instances based on tag values.
- B. Create a Systems Manager State Manager association to run the AmazonCloudWatch-ManageAgent Systems Manager Run Command document. Select Systems Manager as an optional configuration source. Target the instances based on tag values.
- C. Store the CloudWatch agent configuration file in an Amazon S3 bucket.
- D. Store the contents of the CloudWatch agent configuration file in Systems Manager Parameter Store.
- E. Store the contents of the CloudWatch agent configuration file in Systems Manager OpsCenter.

**Answer: B, D**

**Why correct:**

- **D:** Parameter Store is the supported central location for the agent's JSON configuration, so every instance pulls the same definition.
- **B:** A State Manager association runs `AmazonCloudWatch-ManageAgent` with the configuration source set to `ssm` and the configuration location set to the parameter name, targeting the tag `OS=Windows`. State Manager applies the configuration to every tagged instance and reapplies it on a schedule, which prevents drift.

**Why the others are incorrect:**

- **A and C:** The `AmazonCloudWatch-ManageAgent` document accepts `ssm` (Parameter Store) or `default` as its configuration source; it does not take an S3 bucket location.
- **E:** OpsCenter tracks and resolves operational issues (OpsItems); it does not store configuration data.

---

## Question 28

A CloudOps engineer recently configured Amazon S3 Cross-Region Replication (CRR) on an S3 bucket.

Which of the following does this feature replicate to the destination S3 bucket by default?

- A. Objects that are stored in S3 Glacier Flexible Retrieval
- B. Objects in the source S3 bucket for which the bucket owner does not have permissions
- C. Object metadata
- D. Objects that existed before replication was configured

**Answer: C**

**Why correct:** By default, replication copies new objects created after the configuration is added, along with their metadata, tags, and ACLs.

**Why the others are incorrect:**

- **A:** Objects in the S3 Glacier Flexible Retrieval or S3 Glacier Deep Archive storage classes are not replicated.
- **B:** S3 cannot replicate objects that the bucket owner has no permission to read.
- **D:** Existing objects are not replicated automatically; replicating them requires S3 Batch Replication.

---

## Question 29

A CloudOps engineer needs to install the Amazon CloudWatch agent on an Amazon EKS cluster. The EKS cluster is deployed on Amazon EC2 instances. The CloudOps engineer must collect node-level metrics and logs from the containers.

Which solution will meet this requirement with the LEAST operational overhead?

- A. Install the CloudWatch agent on each EC2 instance in the EKS cluster by using AWS Systems Manager.
- B. Configure the CloudWatch agent within the container images that run in the EKS cluster.
- C. Install the CloudWatch agent on the Kubernetes control plane node in the EKS cluster.
- D. Enable and configure the CloudWatch Observability EKS add-on on the EKS cluster.

**Answer: D**

**Why correct:** The add-on installs the CloudWatch agent and Fluent Bit as DaemonSets, so every node, including nodes added later, automatically sends node-level metrics (Container Insights) and container logs to CloudWatch. EKS manages the add-on's installation and version updates.

**Why the others are incorrect:**

- **A:** Installing the agent per instance means managing configuration and updates per node, and a host-level agent does not collect Kubernetes-aware container metrics and logs without extra setup.
- **B:** Building the agent into every image requires rebuilding and maintaining all images, and a per-container agent cannot collect node-level metrics.
- **C:** The EKS control plane is managed by AWS, so there is no control plane node available to install software on.

---

## Question 30

A company wants to launch a group of Amazon EC2 instances that need to communicate with each other with the lowest possible latency.

Which combination of actions should a CloudOps engineer take when launching these instances? (Select TWO)

- A. Launch instances in different VPCs with VPC peering enabled.
- B. Launch instances in a spread placement group.
- C. Launch instances with enhanced networking enabled.
- D. Launch instances in different VPCs with a VPN tunnel.
- E. Launch instances in a cluster placement group.

**Answer: C, E**

**Why correct:**

- **E:** A cluster placement group packs instances close together inside a single Availability Zone, which gives the lowest network latency and highest per-flow throughput between them.
- **C:** Enhanced networking (ENA) uses SR-IOV to provide higher packets per second, lower latency, and lower jitter than the default virtualized network interface.

**Why the others are incorrect:**

- **A:** Splitting instances across VPCs with peering adds routing between networks and does nothing to reduce latency.
- **B:** A spread placement group places each instance on distinct hardware to limit correlated failures; it favors availability, not low latency.
- **D:** A VPN tunnel adds encryption overhead and extra hops, which increases latency.

---

## Question 31

A company is hosting a website on an Amazon EC2 instance that runs in a public subnet inside a VPC. The company uses Amazon CloudWatch Logs for web server log analysis.

A CloudOps engineer has installed and configured the CloudWatch Logs agent on the EC2 instance and has confirmed that the agent is running. However, logs are not showing up in CloudWatch Logs.

Which solution will resolve this issue?

- A. Create an IAM user that has the proper permissions for CloudWatch Logs. Create an IAM instance profile, and associate it with the IAM user. Associate the instance profile with the EC2 instance.
- B. Modify the EC2 instance security group rules to allow inbound traffic on port 80.
- C. Modify the VPC's network ACL rules for the public subnet to allow inbound traffic on port 80.
- D. Create an IAM role that has the proper permissions for CloudWatch Logs. Create an IAM instance profile, and associate it with the IAM role. Associate the instance profile with the EC2 instance.

**Answer: D**

**Why correct:** The agent is installed and running, so the missing piece is authorization. The agent needs credentials to call the CloudWatch Logs API, and on EC2 those come from an IAM role delivered through an instance profile, which supplies temporary, automatically rotated credentials.

**Why the others are incorrect:**

- **A:** An instance profile is a container for an IAM role; it cannot be associated with an IAM user.
- **B:** Inbound port 80 is for web traffic. The agent sends logs outbound over HTTPS (443), so inbound rules do not affect log delivery.
- **C:** Same reason: inbound port 80 on the network ACL is unrelated to the agent's outbound calls.

---

## Question 32

A CloudOps engineer has enabled AWS CloudTrail in an AWS account. If CloudTrail is disabled, it must be re-enabled immediately.

What should the CloudOps engineer do to meet these requirements WITHOUT writing custom code?

- A. Create an AWS Config rule that is invoked when CloudTrail configuration changes. Configure the rule to invoke an AWS Lambda function to enable CloudTrail.
- B. Create an AWS Config rule that is invoked when CloudTrail configuration changes. Apply the AWS-ConfigureCloudTrailLogging automatic remediation action.
- C. Add the AWS account to AWS Organizations. Enable CloudTrail in the management account.
- D. Create an Amazon EventBridge hourly rule with a schedule pattern to run an AWS Systems Manager Automation runbook to enable CloudTrail.

**Answer: B**

**Why correct:** The AWS Config managed rule detects when CloudTrail is disabled and marks the account noncompliant. Automatic remediation then runs the AWS-managed Systems Manager Automation runbook `AWS-ConfigureCloudTrailLogging`, which turns logging back on. Both the rule and the runbook are prebuilt, so no code is written.

**Why the others are incorrect:**

- **A:** It would work, but the Lambda function is custom code, which the requirement rules out.
- **C:** Enabling CloudTrail in a management account does not by itself re-enable a trail that was turned off in this account.
- **D:** An hourly schedule can leave CloudTrail disabled for up to an hour, so it is not immediate.

---

## Question 33

A company deployed a new web application on multiple Amazon EC2 instances behind an Application Load Balancer (ALB). The EC2 instances run in an Auto Scaling group. Users report that they are frequently being prompted to log in.

What should a CloudOps engineer do to resolve this issue?

- A. Redeploy the EC2 instances in a spread placement group.
- B. Replace the ALB with a Network Load Balancer (NLB).
- C. Enable sticky sessions (session affinity) for the target group of EC2 instances.
- D. Configure an Amazon CloudFront distribution with the ALB as the origin.

**Answer: C**

**Why correct:** The application stores session state locally on each instance. The ALB distributes requests across instances, so a user's next request can land on an instance with no record of their session, which forces a new login. Sticky sessions use a cookie to route each user to the same instance for the duration of the session.

**Why the others are incorrect:**

- **A:** A spread placement group controls which hardware the instances run on; it has no effect on request routing or session state.
- **B:** An NLB works at layer 4 and has no cookie-based session affinity.
- **D:** CloudFront caches and delivers content from the edge; requests still reach different instances behind the ALB.

---

## Question 34

A company recently migrated its three-tier web application to AWS. The application runs on Amazon EC2 instances that are in an Auto Scaling group. A CloudOps engineer must create a monitoring dashboard to watch CPU and network utilization for each instance at 1-minute intervals.

How can the CloudOps engineer meet this requirement?

- A. Create an Amazon CloudWatch dashboard with basic monitoring.
- B. Create an Amazon CloudWatch dashboard, and enable detailed monitoring.
- C. Set up AWS CloudTrail with a dashboard on Amazon Quick Sight.
- D. Use the AWS Health Dashboard.

**Answer: B**

**Why correct:** Detailed monitoring makes EC2 publish its metrics, including `CPUUtilization`, `NetworkIn`, and `NetworkOut`, to CloudWatch at 1-minute intervals. A CloudWatch dashboard then graphs them per instance. For an Auto Scaling group, detailed monitoring is enabled in the launch template.

**Why the others are incorrect:**

- **A:** Basic monitoring publishes EC2 metrics at 5-minute intervals.
- **C:** CloudTrail records API activity, not performance metrics.
- **D:** The AWS Health Dashboard reports AWS service events and account health notifications, not instance-level metrics.

---

## Question 35

A CloudOps engineer is managing an application that runs on Amazon EC2 instances behind an Application Load Balancer. The instances run in an Auto Scaling group across multiple Availability Zones. The application stores data in an Amazon RDS MySQL DB instance. The CloudOps engineer must ensure that the application stays available if the database becomes unresponsive.

How can these requirements be met?

- A. Create read replicas for the RDS database and use them in case of a database failure.
- B. Keep a separate RDS database running and switch the endpoint in the web application if a failure occurs.
- C. Modify the RDS instance to be a Multi-AZ deployment.
- D. Create a new RDS instance from the snapshot of the original RDS instance if a failure occurs.

**Answer: C**

**Why correct:** Multi-AZ keeps a synchronously replicated standby in another Availability Zone. If the primary becomes unresponsive, RDS fails over automatically and repoints the same DNS endpoint, so the application reconnects with no configuration change and no data loss.

**Why the others are incorrect:**

- **A:** Read replicas use asynchronous replication and are meant for read scaling. Promotion is manual, the endpoint differs, and recent writes can be lost.
- **B:** A separate database needs its own data synchronization and a manual endpoint change, which adds downtime and operational work.
- **D:** Restoring from a snapshot takes a long time, loses data written since the snapshot, and produces a new endpoint.

---

## Question 36

A team is using Amazon EC2 instances to conduct a load test. The instance type and AWS Region are specified in the requirements for the load test and cannot be changed. The EC2 instances use Amazon EBS volumes. As the team is scaling additional instances, the team encounters an InstanceLimitExceeded error.

What can the team do to resolve this error?

- A. Run the test in a different Availability Zone.
- B. Terminate the EC2 instance. Relaunch the instance.
- C. Detach the EBS volume. Relaunch the instance.
- D. Increase the service quota for Amazon EC2.

**Answer: D**

**Why correct:** `InstanceLimitExceeded` means the account has reached its EC2 On-Demand quota for that instance family in the Region. The quota is measured in vCPUs per Region, so the fix is to request an increase through Service Quotas.

**Why the others are incorrect:**

- **A:** The quota applies to the whole Region, so another zone hits the same limit. (A zone running out of capacity produces `InsufficientInstanceCapacity`, a different error.)
- **B:** Terminating and relaunching leaves the count unchanged.
- **C:** EBS volumes have their own quotas and are unrelated to the instance limit.

---

## Question 37

A CloudOps engineer needs to allow an IAM role in account A to be assumed by AWS services in account B to access resources.

Which action should the CloudOps engineer take to configure the required trust relationship?

- A. Create a role in account A. Specify the account ID for account B in the trust policy.
- B. Create a role in account A. Specify the account ID for account B and the service principal in the trust policy.
- C. Create a role in account A. Specify the Amazon Resource Name (ARN) for the account B root user in the trust policy.
- D. Create a role in account A. Specify the account ID for account B and the IAM user principal in the trust policy.

**Answer: B**

**Why correct:** The role is assumed by AWS services, so the trust policy must name the service principal (for example `lambda.amazonaws.com`). Including account B's ID, typically as an `aws:SourceAccount` condition, limits the trust to that service acting on behalf of account B, which prevents the confused deputy problem.

```json
{
  "Effect": "Allow",
  "Principal": { "Service": "lambda.amazonaws.com" },
  "Action": "sts:AssumeRole",
  "Condition": {
    "StringEquals": { "aws:SourceAccount": "<account-B-id>" }
  }
}
```

**Why the others are incorrect:**

- **A:** The account ID alone trusts IAM principals in account B, not AWS services.
- **C:** The account root ARN is equivalent to trusting the whole account, with the same problem as A.
- **D:** An IAM user principal lets a specific user assume the role, not an AWS service.

---

## Question 38

A CloudOps engineer wants to encrypt an existing Amazon RDS DB instance with AWS KMS.

How should the CloudOps engineer accomplish this goal?

- A. Create a read replica of the unencrypted instance. Encrypt the read replica with the KMS key. Promote the read replica to become the primary instance.
- B. Take a snapshot of the unencrypted instance. Apply the KMS key to the existing instance using the modify-db-instance command. Restart the instance.
- C. Take a snapshot of the unencrypted instance. Create an encrypted copy of the snapshot with the KMS key. Restore the instance from the encrypted snapshot.
- D. Copy the data volumes of the unencrypted instance. Apply the KMS key to the copied data volumes. Start the instance with the encrypted volumes.

**Answer: C**

**Why correct:** RDS encryption can only be enabled when a DB instance is created, so an existing unencrypted instance cannot be encrypted in place. Copying a snapshot lets you specify a KMS key for the copy, and restoring from that encrypted copy creates a new encrypted instance. The application must then be pointed at the new endpoint.

**Why the others are incorrect:**

- **A:** An encrypted read replica cannot be created from an unencrypted source instance.
- **B:** `modify-db-instance` cannot enable encryption on an existing instance.
- **D:** RDS manages its underlying storage, so the data volumes are not accessible to copy, encrypt, or reattach.

---

## Question 39

A CloudOps engineer has restored an Amazon EBS volume from an EBS snapshot. The new EBS volume initially experienced high latency that resolved over time.

What can the CloudOps engineer do to avoid this latency in the future?

- A. Restore to a different AWS Region.
- B. Restore to a larger volume with Provisioned IOPS.
- C. Select the EBS fast snapshot restore feature.
- D. Deactivate encryption during the restore.

**Answer: C**

**Why correct:** A volume restored from a snapshot loads its blocks lazily from Amazon S3, so the first read of each block is slow until it has been fetched. Fast snapshot restore (FSR) creates volumes that are fully initialized at creation, so they deliver their provisioned performance immediately. FSR is enabled per snapshot and per Availability Zone and has an hourly charge.

**Why the others are incorrect:**

- **A:** Lazy loading applies in every Region.
- **B:** A larger Provisioned IOPS volume still has to fetch each block from S3 on first access.
- **D:** Encryption does not cause the first-access latency, and a volume restored from an encrypted snapshot cannot be made unencrypted during the restore.

---

## Question 40

A CloudOps engineer wants to manage a web server application with AWS Elastic Beanstalk. The Elastic Beanstalk service must maintain full capacity for new deployments at all times.

Which deployment policies satisfy this requirement? (Select TWO)

- A. All at once
- B. Rolling
- C. Rebuild
- D. Immutable
- E. Rolling with additional batch

**Answer: D, E**

**Why correct:**

- **D. Immutable:** Elastic Beanstalk launches a full set of new instances in a temporary Auto Scaling group alongside the existing ones. The old instances keep serving until the new ones pass health checks, so capacity never drops below 100%.
- **E. Rolling with additional batch:** Elastic Beanstalk launches an extra batch of instances before taking any out of service, so the environment keeps full capacity throughout.

**Why the others are incorrect:**

- **A. All at once:** Deploys to every instance simultaneously, so the application is unavailable during the deployment.
- **B. Rolling:** Takes one batch out of service at a time, so capacity is reduced by the batch size.
- **C. Rebuild:** Not a deployment policy. Rebuilding an environment terminates and recreates all its resources.

---

## Question 41

A company runs a web application on three Amazon EC2 instances behind an Application Load Balancer (ALB). Web traffic increases significantly during the same 9-hour period every day and causes a decrease in the application's performance. A CloudOps engineer must scale the application ahead of the changes in demand to meet a service level agreement (SLA) for application latency.

Which solution will meet these requirements?

- A. Create an Amazon CloudWatch alarm to monitor application latency. Configure an alarm action to increase the size of each EC2 instance if the latency threshold is reached.
- B. Deploy the application to an EC2 Auto Scaling group that uses a target tracking scaling policy. Attach the ALB to the Auto Scaling group.
- C. Deploy the application to an EC2 Auto Scaling group that uses a scheduled scaling policy. Attach the ALB to the Auto Scaling group.
- D. Create an Amazon EventBridge rule to monitor application latency. Configure the rule to add an EC2 instance to the ALB if the latency threshold is reached.

**Answer: C**

**Why correct:** The traffic increase happens at the same time every day, so the demand is predictable. Scheduled scaling raises capacity shortly before the 9-hour period begins and lowers it afterward, so the instances are already in service when the load arrives.

**Why the others are incorrect:**

- **A:** It reacts only after latency has breached the threshold, and resizing an instance requires stopping it, which reduces capacity during peak load.
- **B:** Target tracking is reactive: it scales after the metric moves, and new instances need time to launch and warm up.
- **D:** EventBridge rules match events or schedules; they do not monitor a latency metric, and the approach is still reactive.

---

## Question 42

An application runs on Amazon EC2 instances behind an Application Load Balancer (ALB). The instances run in an Auto Scaling group that terminates unhealthy instances. The Auto Scaling group is configured to determine the health status of EC2 instances by using both EC2 status checks and ALB health checks. The development team wants to analyze the unhealthy instances before termination.

What should a CloudOps engineer do to accomplish this?

- A. Configure an AWS Lambda function to take a snapshot of all instances before they are terminated.
- B. Configure the ALB health check to restart instances instead of terminating them.
- C. Use an Amazon EC2 Auto Scaling lifecycle hook to pause instance termination after the instance has been removed from service.
- D. Implement Amazon EventBridge to capture lifecycle events and invoke an AWS Lambda function for remediation.

**Answer: C**

**Why correct:** A termination lifecycle hook (`autoscaling:EC2_INSTANCE_TERMINATING`) puts the instance in the `Terminating:Wait` state after it is deregistered from the ALB. The instance stays running for the hook's timeout (default 1 hour, extendable up to 48 hours), which gives the team time to examine it.

**Why the others are incorrect:**

- **A:** A snapshot captures only EBS volume contents; it loses memory, running processes, and live state, and it does not delay termination.
- **B:** ALB health checks only report target health and control routing; they cannot restart or terminate instances.
- **D:** Without a lifecycle hook nothing pauses the termination, so the instance is gone before it can be analyzed.

---

## Question 43

A company runs a web application. The company wants to send 70% of inbound web traffic to the us-east-1 AWS Region and 30% of inbound web traffic to the us-east-2 Region. If the application is not reachable in one of the Regions, the traffic must be rerouted to the other Region.

Which solution will meet this requirement?

- A. Use an Amazon Route 53 weighted routing policy with a 70/30 ratio. Configure a health check.
- B. Use a Network Load Balancer (NLB) with a weighted round robin with a 70/30 ratio. Enable sticky sessions.
- C. Configure an Application Load Balancer (ALB) target group with weighted rules. Enable a health check.
- D. Create two CNAME records in Amazon Route 53. Enable dynamic traffic shaping with a 70/30 ratio.

**Answer: A**

**Why correct:** Weighted routing returns each record in proportion to its weight, so weights of 70 and 30 split traffic between the Regions. Associating a health check with each record makes Route 53 stop returning an unhealthy record, which sends all traffic to the remaining healthy Region.

**Why the others are incorrect:**

- **B:** An NLB operates inside a single Region and cannot distribute traffic across Regions; sticky sessions do not provide failover.
- **C:** ALB weighted target groups split traffic within one Region, not between Regions.
- **D:** Route 53 has no "dynamic traffic shaping" feature, and plain CNAME records provide neither a weighted split nor health-based failover.

---

## Question 44

A company is implementing a custom monitoring service that is based on machine learning. The monitoring service consumes Amazon EventBridge events that Amazon EC2 Auto Scaling generates. The company has configured an EventBridge rule to react to the events. The monitoring service detects anomalous behavior such as unanticipated scaling events and is configured as an EventBridge API destination.

During testing, the company discovers that the monitoring service is not receiving events. However, Amazon CloudWatch shows that the EventBridge rule is being invoked.

A CloudOps engineer must implement a solution to retrieve client error details to help resolve this issue.

Which solution will meet this requirement with the MOST operational efficiency?

- A. Create an EventBridge archive for the event pattern to replay the events. Increase the logging in Amazon CloudWatch Logs. Use replay to invoke the monitoring service.
- B. Configure the EventBridge rule to detect all unanticipated scaling events and to send the messages to an Amazon SNS topic. Subscribe the CloudOps engineer's email address to the SNS topic. Analyze the email messages.
- C. Create a second EventBridge rule for the same event pattern. Create an AWS Lambda function as a target of the second EventBridge rule. Program the Lambda function to invoke the monitoring service and to record the results to Amazon CloudWatch Logs. Examine the errors in the logs.
- D. Create an Amazon SQS standard queue as a dead-letter queue. Add the SQS queue as a target of the EventBridge rule. Use the messages in the SQS queue for debugging. Analyze the error messages and error codes that the monitoring service returns.

**Answer: D**

**Why correct:** The rule is being invoked, so the failure is in delivery to the API destination. When EventBridge cannot deliver an event, it sends the event to the target's dead-letter queue and adds message attributes describing the failure, including `ERROR_CODE`, `ERROR_MESSAGE`, `RULE_ARN`, and `TARGET_ARN`. Those are the client error details needed, and the queue requires no custom code.

**Why the others are incorrect:**

- **A:** An archive and replay only resend the events; the replayed deliveries fail the same way and no error details are captured.
- **B:** An SNS email shows the event content, not the error returned on delivery.
- **C:** A Lambda function could capture the response, but it means custom code and a duplicate rule to maintain.

---

## Question 45

A company has an online gaming application that is experiencing increased usage. The application stores data in a single Amazon DynamoDB table. Forecasts indicate that the application will receive more than 2 million requests each second.

The load on the DynamoDB table consists mostly of read operations. The reads can have eventual consistency. A CloudOps engineer must implement a solution to keep the application's response times as low as possible.

Which solution will meet these requirements?

- A. Load the data into the Amazon S3 Standard storage class. Create an accelerator in AWS Global Accelerator for the application.
- B. Create a DynamoDB Accelerator (DAX) cluster. Configure the application to use the DAX client.
- C. Create an Amazon RDS Proxy. Configure the application to access DynamoDB by using the RDS Proxy.
- D. Configure the application to use strongly consistent reads from the DynamoDB table.

**Answer: B**

**Why correct:** DAX is an in-memory, write-through cache for DynamoDB that serves eventually consistent reads in microseconds instead of single-digit milliseconds and scales to millions of requests per second. The workload is read-heavy and tolerates eventual consistency, which is what DAX serves from cache. It is API-compatible with DynamoDB, so the application only swaps in the DAX client.

**Why the others are incorrect:**

- **A:** S3 is object storage, not a low-latency key-value store, and Global Accelerator optimizes network paths; neither speeds up DynamoDB reads.
- **C:** RDS Proxy pools connections for RDS and Aurora databases; it does not work with DynamoDB.
- **D:** Strongly consistent reads have higher latency, consume twice the read capacity, and bypass the DAX cache.

---

## Question 46

A company has a list of pre-approved Amazon Machine Images (AMIs) for developers to use to launch Amazon EC2 instances. However, developers are still launching EC2 instances from unapproved AMIs.

A CloudOps engineer must implement a solution that automatically terminates any instances that are launched from unapproved AMIs.

Which solution will meet this requirement?

- A. Create a custom Amazon Inspector finding to compare a running instance's AMI against the list of pre-approved AMIs. Create an AWS Lambda function that terminates instances. Configure Amazon Inspector to report findings of unapproved AMIs to an Amazon SQS queue to invoke the Lambda function.
- B. Set up an AWS Config managed rule to check if instances are running from AMIs that are on the list of pre-approved AMIs. Configure an automatic remediation action so that an AWS Systems Manager Automation runbook terminates any instances that are noncompliant with the rule.
- C. Store the list of pre-approved AMIs in an Amazon DynamoDB global table that is replicated to all AWS Regions that the developers use. Create Regional EC2 launch templates. Configure the launch templates to check AMIs against the list and to terminate any instances that are not on the list.
- D. Select the Amazon CloudWatch metric that shows all running instances and the AMIs that the instances were launched from. Create a CloudWatch alarm that terminates an instance if the metric shows the use of an unapproved AMI.

**Answer: B**

**Why correct:** The AWS Config managed rule `approved-amis-by-id` (or `approved-amis-by-tag`) evaluates each running instance against the approved AMI list and marks any other instance noncompliant. Automatic remediation then runs the AWS-managed runbook `AWS-TerminateEC2Instance` against the noncompliant instance, with no custom code.

**Why the others are incorrect:**

- **A:** Amazon Inspector scans for software vulnerabilities and network exposure; it has no custom findings for comparing an instance's AMI against an approved list.
- **C:** Launch templates only define launch parameters; they cannot run logic to check an AMI against a table or terminate instances.
- **D:** CloudWatch has no metric that reports which AMI an instance was launched from.

---

## Question 47

A company is hosting a web application on a fleet of Amazon EC2 instances behind an Application Load Balancer. The instances run in an Amazon EC2 Auto Scaling group.

The company decides that it does not want the number of instances to scale. Instead, the company wants the number of instances to be 10.

Which solution meets this requirement and is the MOST operationally efficient?

- A. Modify the Auto Scaling group for the instances. Set the minimum number of instances to 10. Set the maximum number of instances to 10. Set the desired capacity to 10.
- B. Remove the Auto Scaling group. Configure Amazon EventBridge to invoke an AWS Lambda function to launch a new instance when an unhealthy instance is detected.
- C. Modify the Auto Scaling group for the instances. Configure target tracking scaling policies, and set the target to 10.
- D. Remove the Auto Scaling group. Configure an Amazon CloudWatch alarm to invoke an AWS Lambda function to launch a new instance when an unhealthy instance is detected.

**Answer: A**

**Why correct:** With minimum, maximum, and desired capacity all at 10, the group cannot scale in or out, and Auto Scaling still replaces any unhealthy instance automatically to keep the count at 10. It is a configuration change to the existing group with no code.

**Why the others are incorrect:**

- **B:** Rebuilding instance replacement with EventBridge and Lambda means writing and maintaining custom code for something Auto Scaling already does.
- **C:** A target tracking policy adjusts capacity to hold a metric at a target value; it does not fix the instance count.
- **D:** A CloudWatch alarm with a Lambda function has the same custom-code overhead as B and gives up Auto Scaling's built-in health replacement.

---

## Question 48

A company is running a media streaming website that serves users around the world. The website is hosted on Amazon EC2 instances that are behind an Application Load Balancer (ALB).

The company is running its infrastructure redundantly across two AWS Regions. Each Region contains its own separate copy of the website infrastructure. If one Region becomes unusable due to an application error, the company wants to automatically fail over traffic to the other Region.

Which solution will meet these requirements?

- A. Use Amazon Route 53 to set up DNS failover with a latency-based routing policy. Create an alias record with the same name and type for each ALB in each Region. Ensure that Evaluate Health Target is set to Yes for each record.
- B. Use Amazon Route 53 to set up DNS failover with a simple routing policy. Create an alias record with the same name for each ALB in each Region. Ensure that Evaluate Health Target is set to Yes for each record.
- C. Create a health check for the ALB in each Region by using Elastic Load Balancing health checks. Set up DNS failover with a latency-based routing policy for the ALB. Ensure that Evaluate Health Target is set to Yes.
- D. Create a health check for the ALB by using Amazon CloudWatch monitoring. Set up a CloudWatch alarm to launch a DNS failover with an Amazon Route 53 weighted routing policy whenever the ALB becomes unhealthy.

**Answer: A**

**Why correct:** Latency-based routing sends each user to the Region with the lowest latency, which suits a global streaming audience. With Evaluate Target Health enabled on an alias record, Route 53 uses the ALB's own target health: if a Region's ALB has no healthy targets because of an application error, Route 53 stops returning that record and answers with the other Region's ALB. No separate Route 53 health check is needed.

**Why the others are incorrect:**

- **B:** A simple routing policy does not allow multiple records with the same name and type, so it cannot fail over between two Regional ALBs.
- **C:** Elastic Load Balancing health checks are configured on target groups to check instances; they are not health checks you attach to a DNS failover setup. Evaluate Target Health already covers this.
- **D:** A CloudWatch alarm does not launch DNS failover, and a weighted policy needs health checks associated with the records, which this option does not configure.

---

## Question 49

A CloudOps engineer must run a script on a company's production servers to fix an issue. According to company policy, all SSH access to production servers has already been blocked.

How can the CloudOps engineer run the script?

- A. Put the script into the user data of the instances.
- B. Use AWS Systems Manager Session Manager to run the script.
- C. Share and use the Amazon EC2 key pairs to gain access to the servers and run the script.
- D. Configure the script to run as a cron job or a scheduled task on the Amazon EC2 instances.

**Answer: B**

**Why correct:** Session Manager gives shell access through the SSM Agent, which makes an outbound connection to the Systems Manager service. It needs no SSH, no open inbound ports, and no key pairs, so it complies with the policy. Access is controlled by IAM, and sessions can be logged.

**Why the others are incorrect:**

- **A:** User data runs at first launch by default, so it would not run on servers that are already running.
- **C:** Key pairs are for SSH, which is blocked, and sharing keys is a security violation.
- **D:** Creating a cron job or scheduled task on the instances requires access to them in the first place.

---

## Question 50

A company has a key management service in its on-premises data center. The key management service uses an RSA asymmetric encryption algorithm. The company needs to integrate its system with a highly available, secure service in AWS to replace the on-premises service. The keys must be stored in dedicated hardware security modules that are validated by a third party. The company must control these hardware security modules.

Which solution will meet these requirements?

- A. Generate a customer key from AWS KMS. Import the key into the on-premises environment.
- B. Launch an Amazon EC2 instance. Install an application that generates RSA keys. Import the existing keys into the application.
- C. Import the current keys from the on-premises environment into an AWS CloudHSM cluster.
- D. Revoke the current keys. Generate new asymmetric keys in AWS KMS.

**Answer: C**

**Why correct:** CloudHSM provides single-tenant hardware security modules that are FIPS 140 validated by a third party. The company controls the HSMs and their users, and AWS has no access to the key material. A cluster with HSMs in multiple Availability Zones is highly available, and CloudHSM supports RSA asymmetric keys.

**Why the others are incorrect:**

- **A:** AWS KMS keys cannot be exported, so a KMS key cannot be imported into the on-premises environment, and standard KMS uses shared, AWS-managed HSMs.
- **B:** A key-generation application on an EC2 instance stores keys in software, not in a validated HSM, and is not highly available.
- **D:** Standard AWS KMS runs on multi-tenant HSMs managed by AWS, so the company does not control dedicated HSMs.

---

## Question 51

A CloudOps engineer wants to make a file available to the public by using Amazon S3. The CloudOps engineer creates a presigned URL by using the AWS CLI. Users are able to download the file.

After a few days, the CloudOps engineer finds out that users can no longer download the file.

What are the possible reasons that the file is no longer available? (Select TWO)

- A. The presigned URL's expiration date and time have passed.
- B. The S3 object's ACL does not include READ access for the All Users group.
- C. The S3 bucket's Block Public Access settings are enabled.
- D. The S3 object's ACL does not include READ_ACP access for the All Users group.
- E. The CloudOps engineer's access key is no longer valid.

**Answer: A, E**

**Why correct:**

- **A:** Every presigned URL has an expiration time. With the AWS CLI the default is 3,600 seconds, and the maximum for a URL signed with IAM user credentials is 7 days.
- **E:** A presigned URL is signed with the creator's credentials and is only valid while those credentials are. If the access key was deleted, deactivated, or rotated, the URL stops working even before its expiration time.

**Why the others are incorrect:**

- **B:** A presigned URL grants access using the signer's permissions, so the object does not need a public READ ACL.
- **C:** Block Public Access restricts public ACLs and bucket policies; it does not affect presigned URLs, which are authenticated requests.
- **D:** `READ_ACP` allows reading the object's ACL, not the object itself.

---

## Question 52

A company wants to share network resources across two AWS accounts. Account A has an AWS Transit Gateway. The company wants to grant read-only access to the Transit Gateway to users in account B.

Which solution will meet these requirements?

- A. Use IAM to create an IAM role in account B with permissions to view Transit Gateway resources in account A.
- B. Use IAM to create an IAM role in account A with permissions for users in account B to view Transit Gateway resources.
- C. Use AWS Resource Access Manager (AWS RAM) to create an AWS RAM principal in account B. Associate the AWS RAM resource share with the principal.
- D. Use AWS Resource Access Manager (AWS RAM) to create an AWS RAM resource share in account A. Specify the Transit Gateway to share with account B.

**Answer: D**

**Why correct:** AWS RAM is the service for sharing resources such as transit gateways across accounts. The owner (account A) creates the resource share, adds the transit gateway, and names account B as the principal. The managed permission attached to the share controls what account B can do, and the transit gateway appears in account B without account B owning or being able to modify it.

**Why the others are incorrect:**

- **A:** A role in account B cannot grant access to resources owned by account A.
- **B:** A cross-account role would let users assume it to view the resource, but it does not share the transit gateway with account B, which is the stated goal.
- **C:** The resource share is created in the account that owns the resource (account A), and there is no "RAM principal" resource to create; principals are specified in the share.

---

## Question 53

A company expanded its web application to serve a worldwide audience. A CloudOps engineer has implemented a multi-Region AWS deployment for all production infrastructure. The CloudOps engineer must route traffic based on the location of resources.

Which Amazon Route 53 routing policy should the CloudOps engineer use to meet this requirement?

- A. Geolocation routing policy
- B. Latency-based routing policy
- C. Geoproximity routing policy
- D. Multivalue answer routing policy

**Answer: C**

**Why correct:** Geoproximity routing routes traffic based on the geographic location of your resources (and optionally of your users), and a bias value shifts more or less traffic toward a given resource. "Based on the location of resources" is the wording AWS uses for this policy.

**Why the others are incorrect:**

- **A:** Geolocation routing is based on the location of the users (where the DNS queries originate), not the resources.
- **B:** Latency-based routing sends users to the Region with the lowest network latency, which is a performance measurement, not a location.
- **D:** Multivalue answer routing returns up to eight healthy records chosen at random; it does not consider location.

---

## Question 54

A CloudOps engineer needs to delete an AWS CloudFormation stack that is no longer in use. The CloudFormation stack is in the DELETE_FAILED state. The CloudOps engineer has validated the permissions that are required to delete the CloudFormation stack.

Which of the following are possible causes of the DELETE_FAILED state? (Select TWO)

- A. There are Amazon S3 buckets that still contain objects in the stack.
- B. The stack was deployed with the --disable-rollback option.
- C. There are additional resources associated with a security group in the stack.
- D. The configured timeout to delete the stack was too low for the delete operation to complete.
- E. The stack contains nested stacks that must be manually deleted first.

**Answer: A, C**

**Why correct:**

- **A:** CloudFormation can only delete an empty S3 bucket. If a bucket in the stack still contains objects, the bucket deletion fails and the stack goes to `DELETE_FAILED`.
- **C:** A security group cannot be deleted while other resources still reference it, such as network interfaces or instances created outside the stack.

**Why the others are incorrect:**

- **B:** `--disable-rollback` controls whether a failed stack creation rolls back; it has no effect on deletion.
- **D:** There is no configurable timeout for stack deletion; the timeout setting applies to stack creation.
- **E:** CloudFormation deletes nested stacks automatically as part of deleting the parent stack.

---

## Question 55

A company has hundreds of Amazon EC2 instances in its environment. The company's security team wants to make sure that all the security patches and critical patches are installed on all the EC2 instances. A CloudOps engineer needs to automate this process.

How can the CloudOps engineer meet this requirement?

- A. Schedule an AWS Lambda function that uses Amazon CloudWatch to retrieve a list of the current software releases that are installed on the EC2 instances. Configure the Lambda function to patch the instances that need the security updates and critical updates.
- B. Configure AWS Systems Manager Patch Manager to apply the patches on a schedule. Use a predefined patch baseline that approves all patches that are classified as security updates or critical updates.
- C. Schedule an AWS Lambda function that uses AWS Config to retrieve a list of the current software releases that are installed on the EC2 instances. Configure the Lambda function to patch the instances that need the security updates and critical updates.
- D. Use the EC2 console to retrieve a list of the current software releases that are installed on the EC2 instances. Add a tag to the EC2 instances that need patch updates. Schedule an AWS Lambda function to patch the instances based upon the tag.

**Answer: B**

**Why correct:** Patch Manager is the AWS service built for this. A predefined patch baseline auto-approves patches classified as security or critical updates, and a maintenance window or patch policy scans and installs them on a schedule across all managed instances. It also reports patch compliance, with no custom code.

**Why the others are incorrect:**

- **A:** CloudWatch collects metrics and logs; it does not inventory installed software, and a patching Lambda function is custom code to maintain.
- **C:** AWS Config records resource configurations, not the operating system's installed patches, with the same custom-code overhead.
- **D:** The EC2 console does not list installed software releases, and manually tagging hundreds of instances is not automation.

---

## Question 56

A company uses AWS Lambda functions to process data from various sources. The company must configure Amazon EventBridge rules to invoke the Lambda functions. Each function should be invoked on a schedule or when specific events occur from each of the event sources.

Which solution will meet these requirements with the LEAST operational overhead?

- A. Create separate EventBridge rules for each schedule or event source. Configure each rule to invoke the appropriate Lambda function.
- B. Use AWS Step Functions to orchestrate the invocation of the Lambda functions based on schedules and event sources.
- C. Create a single Lambda function that is invoked by the EventBridge rule. Configure the function to check the schedules in an Amazon DynamoDB table to determine which processing logic to invoke.
- D. Create a single EventBridge rule with a cron expression schedule and multiple event patterns. Configure the rule to invoke different Lambda functions based on the schedule or event that triggers the rule.

**Answer: A**

**Why correct:** An EventBridge rule is either a schedule or an event pattern, and its targets receive every event the rule matches. One rule per schedule or event source, each targeting the right Lambda function, is the native design: no custom code, and each rule can be changed or disabled independently.

**Why the others are incorrect:**

- **B:** Step Functions orchestrates multi-step workflows; using it only to route invocations adds a state machine to build and maintain.
- **C:** A dispatcher function with schedules stored in DynamoDB is custom routing logic to write, test, and operate, plus an extra table.
- **D:** A single rule cannot combine a schedule with event patterns, and a rule cannot choose different targets based on which event matched.

---

## Question 57

A company has a web application that runs on Amazon EC2 instances behind an Application Load Balancer (ALB). The company needs to configure health checks to verify that the target is healthy.

Which health check configuration will meet these requirements?

- A. Configure an ALB health check that uses an application endpoint to verify functionality and then returns an HTTP 200 status code.
- B. Configure an ALB health check that uses the /ping endpoint on the target group and checks for a response within 10 seconds.
- C. Configure an ALB health check that uses the ICMP protocol to verify network connectivity and the response capability of the instances.
- D. Configure an ALB health check that uses the TCP protocol on port 80 of the instances and checks for a response within 10 seconds.

**Answer: A**

**Why correct:** ALB health checks are HTTP or HTTPS requests to a path on each target, and a target is healthy when it returns the expected status code (200 by default). Pointing the check at an endpoint that exercises the application confirms the application itself is working, not just that the instance is up.

**Why the others are incorrect:**

- **B:** A `/ping` endpoint only shows the web server responds; it does not verify application functionality, and a response within a time limit alone does not confirm the status code.
- **C:** ALB health checks do not support ICMP, and a ping would only test network reachability.
- **D:** ALB target groups do not support TCP health checks (those belong to Network Load Balancers), and an open port 80 does not prove the application works.

---

## Question 58

A company stores data in an Amazon S3 bucket. The company must ensure that some specific objects are not deleted or overwritten for 10 years to comply with local regulations. The company wants to use Amazon S3 Object Lock to protect the objects.

Which solution will meet these requirements?

- A. Configure object ACLs and an S3 Lifecycle configuration to retain objects. Set up S3 Object Lock in governance mode.
- B. Enable versioning for the S3 bucket. Set up S3 Object Lock in compliance mode.
- C. Enable encryption for the S3 bucket that uses a custom AWS KMS key to restrict deletions or data overwriting. Apply a legal hold to the objects.
- D. Configure the S3 bucket to require multi-factor authentication (MFA) for delete operations to prevent any accidental deletions.

**Answer: B**

**Why correct:** S3 Object Lock requires versioning on the bucket. In compliance mode, a protected object version cannot be overwritten or deleted by any user, including the account root user, and the retention period cannot be shortened until it expires. A 10-year retention period on the specific objects satisfies the regulation.

**Why the others are incorrect:**

- **A:** In governance mode, users with the `s3:BypassGovernanceRetention` permission can override the lock, so it does not guarantee retention. ACLs and lifecycle rules do not prevent deletion.
- **C:** KMS encryption controls who can decrypt data; it does not prevent deletion or overwriting. A legal hold has no retention period and can be removed by anyone with the `s3:PutObjectLegalHold` permission.
- **D:** MFA delete adds an authentication step, but an authorized user with the MFA device can still delete objects, and it does not use Object Lock.

---

## Question 59

A CloudOps engineer implemented the following bucket policy to allow only the corporate IP address range of 54.240.143.0/24 to access objects in an Amazon S3 bucket:

```json
{
    "Version": "2012-10-17",
    "Id": "S3PolicyId1",
    "Statement": [
        {
            "Sid": "S3Allow",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::examplebucket",
                "arn:aws:s3:::examplebucket/*"
            ]
        },
        {
            "Sid": "IPAllow",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::examplebucket",
                "arn:aws:s3:::examplebucket/*"
            ],
            "Condition": {
                "NotIpAddress": {
                    "aws:SourceIp": "54.240.143.0/24"
                }
            }
        }
    ]
}
```

Some employees are reporting that they are able to access the S3 bucket from IP addresses outside the corporate IP address range.

How can the CloudOps engineer address this issue?

- A. Modify the Condition operator to include both NotIpAddress and IpAddress to prevent unauthorized access to the S3 bucket.
- B. Change Effect from Allow to Deny in the second statement of the policy to deny requests not from the source IP range.
- C. Modify the IAM policy instead of the bucket policy to restrict users from accessing the bucket based on their source IP addresses.
- D. Modify the Condition element from the IAM policy to aws:StringEquals instead of aws:SourceIp.

**Answer: B**

**Why correct:** The second statement currently allows requests that do not come from 54.240.143.0/24, which is the opposite of the intent. Changing it to `Deny` with the same `NotIpAddress` condition blocks every request from outside the corporate range, and an explicit deny overrides any allow, including the first statement and any IAM policy.

```json
{
    "Sid": "IPDeny",
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": [
        "arn:aws:s3:::examplebucket",
        "arn:aws:s3:::examplebucket/*"
    ],
    "Condition": {
        "NotIpAddress": { "aws:SourceIp": "54.240.143.0/24" }
    }
}
```

Caveat about the policy as written: the first statement allows `s3:*` to everyone with no condition, so after the fix anyone inside the corporate range has full access, including anonymous requests from that range.

**Why the others are incorrect:**

- **A:** Using both `IpAddress` and `NotIpAddress` in one condition block requires both to be true, which is contradictory, and the statement would still be an allow.
- **C:** IAM policies only apply to the account's own identities; the bucket policy's unconditional allow to `Principal: "*"` would still grant access from any IP.
- **D:** `aws:StringEquals` is not a condition key. `aws:SourceIp` is the correct key, and it belongs with the IP address operators.

---

## Question 60

A company uses AWS Organizations to manage its multi-account environment. The organization contains a dedicated account for security and a dedicated account for logging. A CloudOps engineer needs to implement a centralized solution that provides alerts when a resource metric in any account crosses a standard defined threshold.

Which solution will meet these requirements?

- A. Deploy an AWS CloudFormation stack set to the accounts in the organization. Use a template that creates the required Amazon CloudWatch alarms and references an Amazon SNS topic in the logging account with publish permissions for all the accounts.
- B. Deploy an AWS Lambda function on a cron job in each account. Configure the Lambda function to read resources that are in the account and to invoke an Amazon SNS topic if any metrics cross the defined threshold.
- C. Deploy an AWS CloudFormation stack in each account. Use the stack to deploy the required Amazon CloudWatch alarms and the required Amazon SNS topic.
- D. Deploy an AWS CloudFormation change set to the organization. Use a template to create the required Amazon CloudWatch alarms and to send alerts to a verified Amazon SES identity.

**Answer: A**

**Why correct:** StackSets integrates with AWS Organizations to deploy one template to every account, including accounts that join later, so all accounts get the same alarms with the same thresholds. Each alarm publishes to a single SNS topic in the logging account, which centralizes the alerts. The topic's access policy must allow the member accounts to publish.

**Why the others are incorrect:**

- **B:** A custom Lambda function on a schedule in every account is code to deploy and maintain per account, and it polls on an interval instead of alerting when a threshold is crossed.
- **C:** A separate stack and SNS topic in each account must be deployed and updated account by account, and the alerts are not centralized.
- **D:** A change set previews changes to a single stack; it does not deploy across an organization, and CloudWatch alarms cannot send to an SES identity directly.

---

## Question 61

A CloudOps engineer created an AWS CloudFormation template that provisions an Amazon EventBridge rule that invokes an AWS Lambda function. The Lambda function is designed to write event details to an Amazon CloudWatch log group. The function has permissions to write events to Amazon CloudWatch Logs. However, the CloudOps engineer discovered that the Lambda function is not running.

How should the CloudOps engineer resolve the problem?

- A. Update the CloudFormation stack to include an AWS::IAM::Role resource with the required IAM permissions for the function. Assign the role as the function execution role.
- B. Update the CloudFormation stack to include an AWS::IAM::Role resource with the required IAM permissions for EventBridge to invoke the function. Assign the role to the EventBridge rule.
- C. Update the CloudFormation stack with an AWS::Lambda::Permission resource to ensure lambda.amazonaws.com has permissions to invoke the function.
- D. Update the CloudFormation stack with an AWS::Lambda::Permission resource to ensure events.amazonaws.com has permissions to invoke the function.

**Answer: D**

**Why correct:** EventBridge invokes Lambda through the function's resource-based policy, so the function must grant `lambda:InvokeFunction` to the `events.amazonaws.com` service principal. The console adds this permission automatically when you create the rule, but CloudFormation does not, so the template needs an explicit `AWS::Lambda::Permission` resource.

```yaml
InvokePermission:
  Type: AWS::Lambda::Permission
  Properties:
    FunctionName: !Ref MyFunction
    Action: lambda:InvokeFunction
    Principal: events.amazonaws.com
    SourceArn: !GetAtt MyRule.Arn
```

**Why the others are incorrect:**

- **A:** The execution role governs what the function can do once it runs, and it already has CloudWatch Logs permissions. The function is not being invoked at all.
- **B:** Lambda targets are authorized through the function's resource-based policy, not through an IAM role on the rule.
- **C:** `lambda.amazonaws.com` is the Lambda service principal, not the service doing the invoking.

---

## Question 62

A global company handles a large amount of personally identifiable information (PII) through an internal web portal. The company's application runs in a corporate data center that is connected to AWS through an AWS Direct Connect connection. The application stores the PII in Amazon S3. According to a compliance requirement, traffic from the web portal to Amazon S3 must not travel across the internet.

What should a CloudOps engineer do to meet the compliance requirement?

- A. Set up a range of VPC network ACLs to redirect traffic to the internal S3 address.
- B. Provision an interface VPC endpoint for Amazon S3. Modify the application to use the interface endpoint.
- C. Configure AWS Network Firewall to redirect traffic to the internal S3 address.
- D. Modify the application to use the S3 path-style endpoint.

**Answer: B**

**Why correct:** An interface endpoint (AWS PrivateLink) places network interfaces with private IP addresses in the VPC. Those addresses are reachable from the corporate data center over the Direct Connect private connection, so the portal's traffic to S3 stays on the private link and the AWS network. The application uses the endpoint-specific DNS name.

This is the case where the interface type is needed instead of a gateway endpoint: gateway endpoints work through VPC route tables and cannot be used from on-premises networks (compare Question 18).

**Why the others are incorrect:**

- **A:** Network ACLs only allow or deny traffic at the subnet boundary; they cannot redirect traffic.
- **C:** Network Firewall inspects and filters traffic; it does not provide a private path to S3.
- **D:** Path-style addressing only changes the URL format; requests still go to the public S3 endpoint.

---

## Question 63

A company is running workloads on Amazon EC2 instances that are in a single AWS Region. The company needs to create daily backups of each EC2 instance.

A CloudOps engineer must implement a solution to automate the backup creation process.

Which solution will meet this requirement with the LEAST operational overhead?

- A. Use the EC2 console to enable the Auto Recovery option for each instance. Schedule the Auto Recovery option to run every 24 hours.
- B. Create a shell script that uses the AWS CLI. Configure the shell script to list all the instances and to create a snapshot of each instance. Launch a new instance to host the shell script. Set up a cron job to run the shell script every 24 hours.
- C. Use AWS Backup to create a backup plan that uses a daily default template. Specify the EC2 instances as the resources to back up.
- D. Create a shell script that creates a daily cron job on the instances. Configure the cron job to use the AWS CLI to create a snapshot of each instance. Ensure that the instance profile has the required permissions to create a snapshot. Add the shell script to run as part of the instance user data.

**Answer: C**

**Why correct:** AWS Backup is a managed service that schedules backups, applies retention, and monitors backup jobs. A backup plan built from the daily template, with the EC2 instances assigned by ID or by tag, creates a backup of each instance every day with no scripts or servers to maintain.

**Why the others are incorrect:**

- **A:** Auto recovery restarts an instance on new hardware after a system status check failure; it does not create backups and cannot be scheduled.
- **B:** A script on a dedicated instance means an extra server to pay for, patch, and monitor, plus code to maintain, and it is a single point of failure.
- **D:** A cron job on every instance spreads custom scripts and snapshot permissions across the fleet, with no central scheduling, retention, or monitoring.

---

## Question 64

An application accesses data through a file system interface. The application runs on Amazon EC2 instances in multiple Availability Zones, all of which must share the same data. Although the amount of data is currently small, the company anticipates that it will grow to tens of terabytes over the lifetime of the application.

What is the MOST scalable storage solution to meet this requirement?

- A. Connect a large Amazon EBS volume to multiple instances and schedule snapshots.
- B. Launch an EC2 instance and share data using SMB/CIFS or NFS.
- C. Deploy Amazon EFS in the VPC and create mount targets in multiple subnets.
- D. Deploy an AWS Storage Gateway cached volume on Amazon EC2.

**Answer: C**

**Why correct:** Amazon EFS is a managed NFS file system that many EC2 instances can mount at the same time. A mount target in a subnet in each Availability Zone gives every instance access to the same data. Storage grows and shrinks automatically up to petabytes, so there is no capacity to provision.

**Why the others are incorrect:**

- **A:** An EBS volume exists in one Availability Zone. Multi-Attach works only for Provisioned IOPS volumes within that single zone and needs a cluster-aware file system, and a volume has a fixed provisioned size.
- **B:** A self-managed file server on one instance is a single point of failure and a throughput bottleneck, and its storage must be resized manually.
- **D:** A Storage Gateway cached volume presents iSCSI block storage intended for on-premises hybrid use; it is not a shared file system for EC2 instances across zones.

---

## Question 65

A CloudOps engineer is receiving alerts related to high CPU utilization of an Amazon ElastiCache (Memcached) cluster.

Which remediation steps should be taken to resolve this issue? (Select TWO)

- A. Vertically scale the ElastiCache cluster by changing the node type.
- B. Add a load balancer to route traffic to the ElastiCache cluster.
- C. Add a larger Amazon EBS volume to the ElastiCache cluster nodes.
- D. Create an Auto Scaling group for the ElastiCache cluster.
- E. Add additional worker nodes to the ElastiCache cluster.

**Answer: A, E**

**Why correct:**

- **A:** Scaling up to a larger node type gives each node more vCPUs. Memcached is multithreaded, so it can use the additional cores.
- **E:** Adding nodes scales the cluster out. Memcached partitions keys across nodes, so more nodes spread the request load and lower CPU utilization on each one.

**Why the others are incorrect:**

- **B:** ElastiCache clusters are not placed behind a load balancer; clients connect to the nodes directly and distribute keys with client-side hashing or Auto Discovery.
- **C:** Memcached is an in-memory store, and ElastiCache nodes have no customer-managed EBS volumes. Disk size has no effect on CPU utilization.
- **D:** ElastiCache nodes are managed by the service and cannot be put in an EC2 Auto Scaling group.
