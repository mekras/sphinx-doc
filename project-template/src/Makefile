# Вы можете задать эти переменные из командной строки, а первые две через окружение.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SPHINXPROJ    = ВАШ_ПРОЕКТ
SOURCEDIR     = pages
BUILDDIR      = /opt/build

.DEFAULT_GOAL ::= help

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Общая цель: перенаправляет все неизвестные цели в Sphinx, используя новую опцию
# "make mode". $(O) означает сокращение для $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
