import nibabel as nib
import numpy as np
import argparse

labels_to_copy = [17,18,19,48]

def copy_labels(src_path, dst_path, output_path):
    src_nii = nib.load(src_path[0])
    dst_nii = nib.load(dst_path[0])

    src_labels = src_nii.get_fdata()
    dst_labels = dst_nii.get_fdata()

    #Make a copy of dst_nii to preserve original values (our labels)
    new_labels = np.copy(dst_labels)

    #Select the voxels in src_nii that have labels contained on labels_to_copy and have a 
    #zero value in the corresponding indices of dst_nii
    copy_voxels = np.logical_and(np.isin(src_labels,labels_to_copy), dst_labels == 0)

    #Assign selected voxels to the corresponding indices in new array
    new_labels[copy_voxels] = src_labels[copy_voxels]
    
    #Convert the left side's cortex label (42) to 16 to avoid parsing conflicts:
    new_labels[dst_labels == 42] = 16

    #Save new .nii file
    nib.save(nib.Nifti1Image(new_labels,dst_nii.affine,dst_nii.header), output_path[0]+"/merged.nii")

parser = argparse.ArgumentParser()

parser.add_argument('dhcp_segmentation',
                    nargs=1,
                    help='Source labels')

parser.add_argument('your_segmentation',
                    nargs=1,
                    help='Destination labels')

parser.add_argument('output_path',
                    nargs=1,
                    help='Path where output will be located')

#parser.add_argument('labels',
#                    nargs='+',
#                    help='Labels from souce image to conserve in destination image')

args = parser.parse_args()

src = args.dhcp_segmentation
dst = args.your_segmentation
out_dir = args.output_path

#labels_to_copy = args.labels

copy_labels(src,dst,out_dir)


