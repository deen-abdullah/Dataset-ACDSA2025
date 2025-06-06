#ifndef AVL_TREE_H
#define AVL_TREE_H

#include <iostream>

using namespace std;

template <typename Comparable>
class AvlTree
{
public:
	AvlTree() : root(nullptr)
	{ }
	AvlTree(const AvlTree & rhs) : root(nullptr)
	{
		*this = rhs;
	}

	~AvlTree()
	{
		makeEmpty();
	}

    Comparable& find(const Comparable & x)
	{
		return find(x, root);
	}

    const Comparable& findMin() const
	{
		if (isEmpty())
        {
            cerr << "BROKE!" << endl;
        }

		return findMin(root)->element;
	}

    const Comparable& findMax() const
	{
		if (isEmpty())
        {
            cerr << "BROKE!" << endl;
        }

		return findMax(root)->element;
	}

	/*
	* Returns true if x is found in the tree
	*/
    bool contains(const Comparable& x) const
	{
		return contains(x, root);
	}

	/*
	* Test if the tree is logically empty
	* Return true if empty, false otherwise
	*/
	bool isEmpty() const
	{
		return root == nullptr;
	}

	/*
	* Print the tree contents in sorted order
	*/
	void printTree() const
	{
		if (isEmpty())
        {
			cout << "Empty tree" << endl;
        }
		else
        {
			printTree(root);
        }
	}

	/*
	* Make the tree logically empty
	*/
	void makeEmpty()
	{
		makeEmpty(root);
	}

	/*
	* Insert x into the tree; duplicates are ignored
	*/
    void insert(const Comparable& x)
	{
		insert(x, root);
	}

	/*
	* Deep copy
	*/
    const AvlTree& operator=(const AvlTree & rhs)
	{
		if (this != &rhs)
		{
			makeEmpty();
			root = clone(rhs.root);
		}
		return *this;
	}

private:
	struct AvlNode
	{
		Comparable element;
        AvlNode* left;
        AvlNode* right;
        int height;

        AvlNode(const Comparable& theElement, AvlNode* lt,
            AvlNode* rt, int h = 0)
			: element(theElement), left(lt), right(rt), height(h) { }
	};

    AvlNode* root;

	/*
	* Private method to SEARCH and return by reference
	*/
    Comparable& find(const Comparable& x, AvlNode* node)
	{
		if (node == nullptr)
		{
			Comparable a;
			return a;
		}

		else if (x < node->element)
        {
			return find(x, node->left);
        }

		else if (node->element < x)
        {
			return find(x, node->right);
        }
		else
        {
			return node->element;
        }
	}

	/*
	* Internal method to insert into a subtree
	* x is the item to insert
	* t is the node that roots the subtree
	* Set the new root of the subtree
	*/
    void insert(const Comparable& x, AvlNode* & t)
	{
		if (t == NULL)
        {
			t = new AvlNode(x, NULL, NULL);
        }

		else if (x < t->element)
		{
			insert(x, t->left);
			if (height(t->left) - height(t->right) == 2)
            {
				if (x < t->left->element)
                {
					rotateWithLeftChild(t);
                }
				else
                {
					doubleWithLeftChild(t);
                }
            }
		}

		else if (t->element < x)
		{
			insert(x, t->right);
			if (height(t->right) - height(t->left) == 2)
            {
				if (t->right->element < x)
                {
					rotateWithRightChild(t);
                }
				else
                {
					doubleWithRightChild(t);
                }
            }
		}

		else
        {
			;  //Duplicate; do nothing
        }

		t->height = max(height(t->left), height(t->right)) + 1;
	}

	/*
	* Internal method to find the smallest item in a subtree t
	* Return node containing the smallest item
	*/
    AvlNode* findMin(AvlNode* t) const
	{
		if (t == NULL)
        {
			return NULL;
        }

		if (t->left == NULL)
        {
			return t;
        }

		return findMin(t->left);
	}

	/*
	* Internal method to find the largest item in a subtree t
	* Return node containing the largest item
	*/
    AvlNode* findMax(AvlNode* t) const
	{
		if (t != NULL)
        {
			while (t->right != NULL)
            {
				t = t->right;
            }
        }

		return t;
	}

	/*
	* Internal method to test if an item is in a subtree
	* x is item to search for
	* t is the node that roots the tree
	*/
    bool contains(const Comparable& x, AvlNode* t) const
	{
		if (t == NULL)
        {
			return false;
        }

		else if (x < t->element)
        {
			return contains(x, t->left);
        }

		else if (t->element < x)
        {
			return contains(x, t->right);
        }

		else
        {
			return true;
        }
	}
	
	/*
	* Internal method to make subtree empty
	*/
    void makeEmpty(AvlNode* & t)
	{
		if (t != NULL)
		{
			makeEmpty(t->left);
			makeEmpty(t->right);
			delete t;
		}

		t = NULL;
	}

	/*
	* Internal method to print a subtree rooted at t in sorted order
	*/
    void printTree(AvlNode* t) const
	{
		if (t != NULL)
		{
			printTree(t->left);
			cout << t->element << endl;
			printTree(t->right);
		}
	}

	/*
	* Internal method to clone subtree
	*/
    AvlNode* clone(AvlNode* t) const
	{
		if (t == NULL)
        {
			return NULL;
        }

		else
        {
            return new AvlNode(t->element, clone(t->left),
                               clone(t->right), t->height);
        }
    }

	/*
	* Return the height of node t or -1 if NULL
	*/
    int height(AvlNode* t) const
	{
		return t == NULL ? -1 : t->height;
	}

	int max(int lhs, int rhs) const
	{
		return lhs > rhs ? lhs : rhs;
	}

	/*
	* Rotate binary tree node with left child
	* For AVL trees, this is a single rotation for case 1
	* Update heights, then set new root
	*/
    void rotateWithLeftChild(AvlNode* & k2)
	{
        AvlNode* k1 = k2->left;
		k2->left = k1->right;
		k1->right = k2;
		k2->height = max(height(k2->left), height(k2->right)) + 1;
		k1->height = max(height(k1->left), k2->height) + 1;
		k2 = k1;
	}

	/*
	* Rotate binary tree node with right child
	* For AVL trees, this is a single rotation for case 4
	* Update heights, then set new root
	*/
    void rotateWithRightChild(AvlNode* & k1)
	{
        AvlNode* k2 = k1->right;
		k1->right = k2->left;
		k2->left = k1;
		k1->height = max(height(k1->left), height(k1->right)) + 1;
		k2->height = max(height(k2->right), k1->height) + 1;
		k1 = k2;
	}

	/*
	* Double rotate binary tree node: first left child
	* with its right child; then node k3 with new left child
	* For AVL trees, this is a double rotation for case 2
	* Update heights, then set new root
	*/
    void doubleWithLeftChild(AvlNode* & k3)
	{
		rotateWithRightChild(k3->left);
		rotateWithLeftChild(k3);
	}

	/*
	* Double rotate binary tree node: first right child
	* with its left child; then node k1 with new right child
	* For AVL trees, this is a double rotation for case 3
	* Update heights, then set new root
	*/
    void doubleWithRightChild(AvlNode* & k1)
	{
		rotateWithLeftChild(k1->right);
		rotateWithRightChild(k1);
	}
};

#endif
