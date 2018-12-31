class Test < ApplicationRecord
	mount_uploaders :vibration_file, VibrationUploader
end
