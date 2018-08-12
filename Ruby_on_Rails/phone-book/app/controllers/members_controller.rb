class MembersController < ApplicationController
  def index
    @members = Member.all
  end  
  
  def new
    @member = Member.new
  end
  
  def create
  @member = Member.new(params.require(:member).permit(:name, :yomi, :phone))
  @member.save
  end
  
end
