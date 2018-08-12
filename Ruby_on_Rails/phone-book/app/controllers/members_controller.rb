class MembersController < ApplicationController
  def index
    @message = モデル.find(1)
  end
end
