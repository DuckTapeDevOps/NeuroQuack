resource "aws_iam_role" "execution_role" {
  name               = "${var.service_name}-execution-role"
  assume_role_policy = data.aws_iam_policy_document.execution_role.json
}

data "aws_iam_policy_document" "execution_role" {
  statement {
    sid    = "CloudwatchLogsAccess"
    effect = "Allow"
    resources = [
      "arn:aws:logs:${var.region}:${var.account_id}:log-group:/aws/**",
      "*"
    ]
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:CreateLogGroup",
      "logs:DescribeLogStreams"
    ]
  }
  statement {
    sid    = "CloudwatchMetricsAccess"
    effect = "Allow"
    resources = ["arn:aws:logs:${var.region}:${var.account_id}:log-group:/aws/*",
    "*"]
    actions = [
      "cloudwatch:PutMetricData"
    ]
  }
  statement {
    sid       = "ECRAccess"
    effect    = "Allow"
    resources = ["*"]
    actions = [
      "ecr:ListTagsForResource",
      "ecr:ListImages",
      "ecr:DescribeRepositories",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetLifecyclePolicy",
      "ecr:DescribeImageScanFindings",
      "ecr:GetLifecyclePolicyPreview",
      "ecr:GetAuthorizationToken",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:DescribeImages",
      "ecr:GetRepositoryPolicy"
    ]
  }
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "execution_role" {
  name   = "${var.service_name}-policy"
  policy = data.aws_iam_policy_document.execution_role.json
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.execution_role.name
  policy_arn = aws_iam_policy.execution_role.arn
}
