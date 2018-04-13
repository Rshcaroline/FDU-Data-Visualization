# 将最大值换到父节点
def MAX_Heapify(heap, HeapSize, root):
    left = 2*root + 1                   # 左孩子结点
    right = left + 1                    # 右孩子结点
    larger = root                       # 假设父节点是三者中最大的
    # 如果左结点的下标没有越界且左结点比父节点大
    if left < HeapSize and heap[larger] < heap[left]:
        larger = left
    # 如果右结点的下标没有越界且右结点比父节点大
    if right < HeapSize and heap[larger] < heap[right]:
        larger = right
    # 如果做了堆调整，则对结点的值做相应的更换，将父节点变为三者中最大的
    if larger != root:
        heap[larger], heap[root] = heap[root],heap[larger]
        # 不断递归
        MAX_Heapify(heap, HeapSize, larger)

# 构造一个堆
def Build_MAX_Heap(heap):
    HeapSize = len(heap)     # HeapSize用于比较是否已经没有孩子结点
    for i in range((HeapSize -2)//2, -1, -1):     # 从倒数第二层的最后一个结点开始往前
        MAX_Heapify(heap, HeapSize, i)

# 将根节点（最大值）取出与此时的最后一位做对调，然后对前面len-1个节点继续进行对调整过程。
def HeapSort(heap, n):
    Build_MAX_Heap(heap)    # 将数组建成最大堆，此时保证所有的子结点比父节点小
    for i in range(len(heap)-1, len(heap)-1-n, -1):
        heap[0], heap[i] = heap[i], heap[0]
        MAX_Heapify(heap, i, 0)
    return heap

if __name__ == '__main__':
    tst = [5,6,2,3,8,1,8,7,9,0,10,4]
    print(HeapSort(tst, n=5))   # 找第n大的