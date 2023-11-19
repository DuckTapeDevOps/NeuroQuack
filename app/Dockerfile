FROM public.ecr.aws/lambda/python:3.10
ADD requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt
ADD main.py ${LAMBDA_TASK_ROOT}
CMD ["main.handler"]