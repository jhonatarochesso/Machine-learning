class AddFileToTest < ActiveRecord::Migration[5.2]
	def change
		add_column :tests, :vibration_file, :json
	end
end
