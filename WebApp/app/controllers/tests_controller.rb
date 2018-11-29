class TestsController < ApplicationController
	def show
		@test = Test.find(params[:id])
	end

	def new
		@datetimeNow = DateTime.now.strftime()
	end

	def create
		@test = Test.new(test_params)
		
		@test.save
		redirect_to @test
	end


	private

	def test_params
		params.require(:test).permit(:title, :date, :observation, :file)
	end
end
