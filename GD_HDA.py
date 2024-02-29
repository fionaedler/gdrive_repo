import hou, sys, os
import GD_Utils as gd

def uploadFiles():
    print("----- starting upload -----")

    #get upload path and destination from user input
    upload_dir = hou.pwd().parm("file_path").evalAsString()
    dest_folder = hou.pwd().parm("gd_dir").evalAsString()

    # run GD upload
    GD = gd.GDUtils()
    GD.verify_creds()
    parent_id = GD.check_dest_dir(dest_folder)
    GD.upload(upload_dir, dest_folder, parent_id)
    print("----- uploading finished -----")


