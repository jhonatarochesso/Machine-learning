class CreateTests < ActiveRecord::Migration[5.2]
  def change
    create_table :tests do |t|
      t.string :title
      t.datetime :date
      t.text :observation
      t.json :file

      t.timestamps
    end
  end
end
