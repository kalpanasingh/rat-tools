VERSION=$(shell git describe --abbrev=0 --tags)

archive:
	git archive --format=tar --prefix=rat-tools-$(VERSION)/ $(VERSION) | gzip > rat-tools-$(VERSION).tar.gz

.PHONY: archive
