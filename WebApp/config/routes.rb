Rails.application.routes.draw do
	get 'welcome/index'

	resources :tests

	root 'welcome#index'

	get 'tests/start_analisys/:test_id' => 'tests#start_analisys', as: 'test_start_analisys'
end
