import os

# prepare environment
#os.mkdir("host")
#os.system("apt update && apt install xdelta3")
# get patched files
def get_patched_files():
    pass 
    names=["system","vendor","boot"]
    return names


# get current slot
def get_current_slot():
    if os.system("sudo ../bootctl") != "0":
        print("你的设备似乎不是ab分区")
        return "",999
    else :
        sn=os.popen("sudo ../bootctl")
    slot="_a" if sn=="0" else "_b"
    return slot,sn

# get local partitions
def get_local_partitions(names,slot,sn):
    block="/dev/block/by-name/"
    partitions=[ i.replace("\n","") for i in os.popen(f"sudo ls {block}").readlines() ]
    print(partitions)
    for i in names:
        partition_name=i+slot
        print(partition_name)
        if partition_name in partitions:
            os.system(f"sudo dd if={block}{partition_name} of=./host/{partition_name}.img")
    if "super" in partitions:             
        os.system(f"lpunpack -S {sn} {block}super ./host/super/") if slot else os.system(f"lpunpack  {block}super ./host/super/")
    return 

# patch files
def patch_files(names,super):
    for i in names:
        os.system(f"xdelta3 -vds ./host/imgs {i} ./new/{i}.new.img")
    for i in super:
        os.system(f"xdelta3 -vds ./host/super/imgs {i} ./new/{i}.new.img")
    pass


# make super.img



#flash



def main():
    names=get_patched_files()
    slot,sn=get_current_slot()
    get_local_partitions(names,slot,sn)


if __name__ == "__main__":
    main()