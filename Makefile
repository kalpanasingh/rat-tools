VERSION=$(shell git describe --abbrev=0 --tags)

archive:
	git archive --format=tar --prefix=rat-$(VERSION)/ $(VERSION) | gzip > rat-$(VERSION).tar.gz

.PHONY: archive
