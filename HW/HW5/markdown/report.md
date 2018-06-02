---
![BB4E2C22-7AD4-4260-BE9F-46B641E4726A-55966-00001B076C7FF943_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/BB4E2C22-7AD4-4260-BE9F-46B641E4726A-55966-00001B076C7FF943_tmp.JPG)![AF7420DC-CEC3-4AA8-85E7-48586CBA98C0-55966-00001B077604CF0A_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/AF7420DC-CEC3-4AA8-85E7-48586CBA98C0-55966-00001B077604CF0A_tmp.JPG)![AF7420DC-CEC3-4AA8-85E7-48586CBA98C0-55966-00001B077604CF0A_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/AF7420DC-CEC3-4AA8-85E7-48586CBA98C0-55966-00001B077604CF0A_tmp.JPG)typora-copy-images-to: ../markdown
---





# 数据可视化作业5

---

**姓名：** 王艺楷、冉诗菡、何占魁

**学号：** 15300180076、15307130424、51307130175

---

## 任务：局部仿射

>编程实现基于对应关键点的人脸到狒狒脸的形变。提交内容包括：
>
>1. 报告：在报告中清晰描述问题和数据，数据处理的各个步骤及中间结果，代码结构，开发环境，可执行文件使用手册等细节问题；要求在报告中说明每位同学的贡献和工作内容。
>2. Python 代码和可执行文件；代码要有非常清晰的注释。
>3. 数据（如果有用到）。

#### 一、问题和数据：

1. ##### 问题描述：

   在本任务中，庄老师图像被视为源图像(Source Image)称为$S$，狒狒的图像作为目标图像(Targe Image)，称为$T$。通过在图像$S$和$T$中标定对应点或区域，使源图像$S$变形得到和目标图像$T$相似图形结构。从两个角度入手，问题可形式化定义为：

   -  **寻找映射$f$：**已知点或区域集合为$C_S=\{c_1…c_n | c_i \in S.coords\}$与$C_T=\{c_1…c_n | c_i \in T.coords\}$ 。对于$T$图像的任一坐标点$c_T\in T.coords$，如何定义$f: c_T\rightarrow c_S $的映射关系$f$，使得形变图像$T'$具有优秀的效果？
   -  **寻找标定$C$：**已知对于$T$的任意点映射关系$f: c_T\rightarrow c_S$，此处$c_T\in T.coords$且$c_S\in S.coords$。如何定义对应点或者区域的集合 $C_S=\{c_1…c_n | c_i \in S.coords\}$与$C_T=\{c_1…c_n | c_i \in T.coords\}$ ，使得形变图像$T'$具有优秀的效果？

2. ##### 数据描述：

   数据为两张图片：

   -  **源图像：**庄老师的肖像照 `zxh-ape.jpg`
   -  **目标图像：** 狒狒的“肖像照” `ape.png`

![DA679486-4130-426C-AE85-0DEF1F958054](DA679486-4130-426C-AE85-0DEF1F958054.png)



#### 二、数据处理：

1. ##### 算法描述：

   算法思想为**局部仿射**，即**对于标定区域进行局部变换，对于非标定区域实现各局部变换的加权。**算法具体步骤可描述为：

   -  给定点或区域的集合$C_S=\{c_1…c_n | c_i \in S.coords\}$与$C_T=\{c_1…c_n | c_i \in T.coords\}$ 。
   -  遍历目标图像$T$的每一个坐标$c_T\in T.coords$，通过映射$f$获取对应的坐标$c_S\in S.coords$。情况为：

   $$
   c_S = f(c_T)=\left\{
   \begin{aligned}
   &G_i(c_T), & c_T\in C_T,& i=1...n \\
   &\sum^n_{i=1}w_i(c_T)G_i(c_T), & c_T \not \in C_T,&w_i(c_T)=\frac{{d_i(c_T)^{-e}}}{\sum^n_{i=1}{d_i(c_T)^{-e}}} \\
   \end{aligned}
   \right.
   $$

   -  设$h(c, I)$为图像$I$坐标点$c$取其像素值的函数，则对于$\forall  c_T\in T.coords$，都能获取像素值$ h(f(c_T), S)$。
   -  设$T'$为与$T$的尺寸相同的图像，对于$\forall c_T\in T.coords$将$h(c_T, T')$赋值为$h(f(c_T), S)$。由于$f(c_T)$获得的坐标值可能为非整数，因此$h(c,I)$需要插值处理。
   -  若为灰度图像，则重新进行灰度值归一化。得到图像的图像$T'$则为形变图像。

2. ##### 图像处理：

   -  **通道选取：** 因为该任务的目标图像 `ape.png`有四个通道(R, G, B, alpha)，源图像`zxh-ape.jpg`有三个通道(R, G, B)，因此选取前三个通道:

      ```python
      from skimage import io
      # 读取图片
      srcImage = io.imread("zxh-ape.jpg")
      tarImage = io.imread("ape.png")[...,:3]
      ```

   -  **标记点选取：** 我们通过 `PyLab` 的标定函数`ginput()`标定了两张图片的对应点。为了探究标记点疏密程度对局部仿射算法的影响，我们人工标注了稀疏和稠密两套标记点集合：

      -  稀疏标注：每只眼睛2个点；鼻子3个点；嘴巴5个点；共12个点。![F05CF988-713A-4ACE-A072-36D365A1241D](F05CF988-713A-4ACE-A072-36D365A1241D.png)


      -  稠密标注：每只眼睛3个点；鼻子3个点；嘴巴7个点；共16个点。![6BBF9E4E-A844-48D3-9D97-2AA164005EE8](6BBF9E4E-A844-48D3-9D97-2AA164005EE8.png)

3. ##### 变形结果：

   针对上文提到的两个研究问题*“寻找映射”*和*“寻找标定”*，我们进行了两组探究实验。

   - 对于*映射f*，我们探究了参数e的值对于变形结果的影响，发现随着e值变大，形变的力度越大。
   - 对于*标定C*，我们则分别探究了稀疏标定和稠密标定对于变形结果的影响，稠密标定的形变效果更自然。
     - **对于嘴唇：**稠密标定将嘴唇的特征点数量增至 7 个，即用六等分替代原来的四等分。且进一步选取了离鼻子较远的嘴唇下轮廓进行特征点定位。这样的改进帮助嘴唇变得更加平滑。
     - **对于眼睛：**稠密标定加入了眼睛中心作为特征点，这样的改进可以帮助解决眼睛形状的扭曲问题。
     - **对于鼻子：**稠密标定加入了鼻头作为特征点，这样的改进让鼻子从“n”型变为了“m”型。

|          |                            e=0.5                             |                            e=1.0                             |                            e=1.5                             |                            e=2.0                             |                            e=2.5                             |                            e=3.0                             |
| :------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| 稀疏标定 | ![BF7765AD-4B4F-436F-A660-FA63366C26E7-55966-00001B0768EE3102_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/BF7765AD-4B4F-436F-A660-FA63366C26E7-55966-00001B0768EE3102_tmp.JPG) | ![BB4E2C22-7AD4-4260-BE9F-46B641E4726A-55966-00001B076C7FF943_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/BB4E2C22-7AD4-4260-BE9F-46B641E4726A-55966-00001B076C7FF943_tmp.JPG) | ![9471816E-BDB5-4880-A1BF-7D4F44A3F55C-55966-00001B076FDEB390_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/9471816E-BDB5-4880-A1BF-7D4F44A3F55C-55966-00001B076FDEB390_tmp.JPG) | ![60AA8509-64A3-4E57-94C4-B093993E1CAD-55966-00001B077316D8A7_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/60AA8509-64A3-4E57-94C4-B093993E1CAD-55966-00001B077316D8A7_tmp.JPG) | ![AF7420DC-CEC3-4AA8-85E7-48586CBA98C0-55966-00001B077604CF0A_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/AF7420DC-CEC3-4AA8-85E7-48586CBA98C0-55966-00001B077604CF0A_tmp.JPG) | ![15A46487-9E52-4632-B73E-780869D240FA-55966-00001B077918BD33_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/15A46487-9E52-4632-B73E-780869D240FA-55966-00001B077918BD33_tmp.JPG) |
| 稠密标定 | ![8A891903-6E5F-45C4-A2CA-0DCC263AA7C2-55966-00001B0737C96685_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/8A891903-6E5F-45C4-A2CA-0DCC263AA7C2-55966-00001B0737C96685_tmp.JPG) | ![F98468AB-0263-47D5-9593-49C0F8FC4B6A-55966-00001B073CB92A5E_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/F98468AB-0263-47D5-9593-49C0F8FC4B6A-55966-00001B073CB92A5E_tmp.JPG) | ![9FC025CC-A553-46F6-83F8-2924C508095E-55966-00001B07414146C3_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/9FC025CC-A553-46F6-83F8-2924C508095E-55966-00001B07414146C3_tmp.JPG) | ![08FDF8BA-35EC-47FF-B575-F97560D04077-55966-00001B074653B130_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/08FDF8BA-35EC-47FF-B575-F97560D04077-55966-00001B074653B130_tmp.JPG) | ![35B69E4D-6443-4EAF-BEEA-CC5A46963EE2-55966-00001B074B46DE34_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/35B69E4D-6443-4EAF-BEEA-CC5A46963EE2-55966-00001B074B46DE34_tmp.JPG) | ![4E9903D4-E354-49AB-BF15-9002EA3F1589-55966-00001B074FEB98C5_tmp](/Users/ranshihan/Coding/FDU-Data-Visualization/HW/HW5/markdown/4E9903D4-E354-49AB-BF15-9002EA3F1589-55966-00001B074FEB98C5_tmp.JPG) |

3. 


#### 三、代码结构：



#### 四、开发环境：



#### 五、可执行文件使用 



#### 六、合作者贡献

