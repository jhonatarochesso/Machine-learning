class TestsController < ApplicationController
	def index
		@tests = Test.all
	end
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

	def start_analisys
		@test = Test.find(params[:test_id])
		puts "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		puts "START ANALYSIS"
		puts "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		redirect_to @test
	end


	private

	def test_params
		params.require(:test).permit(:title, :date, {vibration_file: []}, :observation)
	end
end
