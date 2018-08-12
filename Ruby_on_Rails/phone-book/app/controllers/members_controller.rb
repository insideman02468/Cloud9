class MembersController < ApplicationController
  def index
    @members = Member.all
  end
  
  def new
    @member = Member.new
  end
  
  def create
    @member = Member.new(member_params)
    @member.save
    redirect_to members_path
  end
  
  def edit
    @member = find_member_by_id
  end
  
  def update
    @member = find_member_by_id
    @member.update(member_params)
    redirect_to members_path
  end
  
  def destroy
    @member = find_member_by_id
    @member.destroy
    redirect_to members_path
  end
  
  private
  def member_params
    params.require(:member).permit(:name, :yomi, :phone)
  end
  
  def find_member_by_id
    Member.find(params[:id])
  end
end