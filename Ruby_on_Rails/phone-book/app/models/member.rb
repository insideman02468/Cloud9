class Member < ApplicationRecord
  validates :name,
    presence: true
    
  validates :phone,
    presence: true,
    format: {with: /\A[0-9-]{,14}\z/}
end
