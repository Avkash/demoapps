import numpy as np
from skimage.util.shape import view_as_blocks


def shuffle_image(im, num):
    map = {}
    rows=cols=num
    blk_size=im.shape[0]//rows

    img_blks=view_as_blocks(im,block_shape=(blk_size,blk_size,3)).reshape((-1,blk_size,blk_size,3))
    print("img_blks.shape: ",  img_blks.shape)

    img_shuff=np.zeros((im.shape[0],im.shape[1],3),dtype=np.uint8)
    print("img_shuff.shape: ", img_shuff.shape)

    a=np.arange(rows*rows, dtype=np.uint8)
    b=np.random.permutation(a)

    map = {k:v for k,v in zip(a,b)}
    print ("Key Map:-\n" + str(map))
  
    for i in range(0,rows):
        for j in range(0,cols):
            x,y = i*blk_size, j*blk_size
            img_shuff[x:x+blk_size, y:y+blk_size] = img_blks[map[i*rows + j]]
            
    shuf_img_blks=view_as_blocks(img_shuff,block_shape=(blk_size,blk_size,3)).reshape((-1,blk_size,blk_size,3))
    print("shuf_img_blks.shape: ",  shuf_img_blks.shape)
            
    return img_shuff,img_blks, map, blk_size, shuf_img_blks

def zigsaw_image(im, num):
    ##map = {}
    rows=cols=num
    blk_size=im.shape[0]//rows

    img_blks=view_as_blocks(im,block_shape=(blk_size,blk_size,3)).reshape((-1,blk_size,blk_size,3))
    ##print("img_blks.shape: ",  img_blks.shape)

    ##img_shuff=np.zeros((im.shape[0],im.shape[1],3),dtype=np.uint8)
    ##print("img_shuff.shape: ", img_shuff.shape)

    ##a=np.arange(rows*rows, dtype=np.uint8)
    ##b=np.random.permutation(a)

    ##map = {k:v for k,v in zip(a,b)}
    ##print ("Key Map:-\n" + str(map))
  
    ##for i in range(0,rows):
    ##    for j in range(0,cols):
    ##        x,y = i*blk_size, j*blk_size
    ##        img_shuff[x:x+blk_size, y:y+blk_size] = img_blks[map[i*rows + j]]
            
    ##shuf_img_blks=view_as_blocks(img_shuff,block_shape=(blk_size,blk_size,3)).reshape((-1,blk_size,blk_size,3))
    ##print("shuf_img_blks.shape: ",  shuf_img_blks.shape)
            
    return blk_size, img_blks

def unscramble_image(im, blk_size, num, input_image_blocks, key_map, sortMap = False):
    map = {}
    rows=cols=num
    print("input_image_blocks.shape: ",  input_image_blocks.shape)

    img_final=np.zeros((im.shape[0],im.shape[1],3),dtype=np.uint8)
    print("img_shuff.shape: ", img_final.shape)

    if (sortMap):
        key_map_sorted = {k: v for k, v in sorted(key_map.items(), key=lambda x: x[1])}
        key_map_sorted_update = list(key_map_sorted.keys())    
        ##print(key_map)
        ##print(key_map_sorted)
        ##print(key_map_sorted.keys())
    else:
        key_map_sorted_update = key_map

    print(key_map_sorted_update)
    for i in range(0,rows):
        for j in range(0,cols):
            x,y = i*blk_size, j*blk_size
            img_final[x:x+blk_size, y:y+blk_size] = input_image_blocks[key_map_sorted_update[i*rows + j]]
    return img_final 