# Build image and run playbook

~~~bash
docker build -t ansible .
docker run -it --rm -v .:/ansible ansible infra.yml
~~~