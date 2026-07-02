.DEFAULT_GOAL := help
PY := python
TF_DIR := infra/terraform
TFVARS ?=

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

setup: ## Create venv and install dependencies (uses uv if present)
	@command -v uv >/dev/null 2>&1 && uv venv .venv || $(PY) -m venv .venv
	@. .venv/bin/activate && (command -v uv >/dev/null 2>&1 && uv pip install -r requirements.txt || pip install -r requirements.txt)
	@echo "Done. Run 'cp .env.example .env' and fill in your backend."

smoke: ## Offline check — build every workflow without calling the model
	@$(PY) smoke_test.py

single:      ## 00 single agent
	@$(PY) demos/00_single_agent.py
sequential:  ## 01 sequential pipeline
	@$(PY) demos/01_sequential.py
concurrent:  ## 02 concurrent review board
	@$(PY) demos/02_concurrent.py
handoff:     ## 03 support handoff
	@$(PY) demos/03_handoff.py
groupchat:   ## 04 headline group chat
	@$(PY) demos/04_group_chat.py
magentic:    ## 05 magentic launch brief
	@$(PY) demos/05_magentic.py
hitl:        ## 06 human-in-the-loop approval
	@$(PY) demos/06_hitl_approval.py

deck: ## Regenerate the PowerPoint deck
	@$(PY) deck/build_deck.py

tf-init: ## Terraform init for Foundry AVM package
	@cd $(TF_DIR) && terraform init -input=false

tf-fmt: ## Terraform fmt check for Foundry AVM package
	@cd $(TF_DIR) && terraform fmt -check -recursive

tf-validate: ## Terraform validate for Foundry AVM package
	@cd $(TF_DIR) && terraform init -backend=false -input=false && terraform validate -no-color

tf-plan: ## Terraform plan for Foundry AVM package (set TFVARS=terraform.tfvars)
	@cd $(TF_DIR) && terraform init -input=false && terraform plan -no-color $(if $(TFVARS),-var-file=$(TFVARS),)

.PHONY: help setup smoke single sequential concurrent handoff groupchat magentic hitl deck tf-init tf-fmt tf-validate tf-plan
