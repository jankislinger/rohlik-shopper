REPO=sputnuc.home:5000
NAME=rohlik-shopper
TAG=$(REPO)/$(NAME)

build:
	docker build -t $(TAG) .

run:
	docker run -p 8000:5000 --name $(NAME) --rm $(TAG)

push:
	docker push $(TAG)

deploy: build push