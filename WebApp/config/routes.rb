Rails.application.routes.draw do
	get 'welcome/index'

	resources :tests

	root 'welcome#index'
end
