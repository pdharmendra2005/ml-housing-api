# Azure UI Live Demo Guide - ML API Deployment

## 🎯 Demo Overview
**Goal**: Deploy ML Housing Price API to Azure AKS using browser UI for live demonstration

## 📋 Prerequisites
- Azure subscription with access
- Your Docker image: `pdharmendra2005/ml-housing-api:withmyvenv`
- Your K8s YAML file: `k8s/fastapi-k8s.yaml`

---

## 🚀 Live Demo Steps (Browser UI)

### Step 1: Create Resource Group
1. **Navigate to Azure Portal** → portal.azure.com
2. **Search**: "Resource Groups" → Click "Create"
3. **Fill in**:
   - Resource group name: `ml-housing-demo-rg`
   - Region: `East US` (or closest to you)
4. **Click**: "Review + create" → "Create"

### Step 2: Create AKS Cluster
1. **Search**: "Kubernetes services" → Click "Create"
2. **Basics tab**:
   - Cluster name: `ml-housing-cluster`
   - Region: Same as resource group
   - Kubernetes version: Latest (default)
   - Node size: `Standard_D2s_v3` (2 vCPUs, 8GiB RAM)
   - Node count: `3`
3. **Node pools tab**: Keep defaults
4. **Networking tab**:
   - Network configuration: `Basic`
   - DNS name prefix: `ml-housing-api`
5. **Review + create** → "Create"
6. **Wait**: 5-10 minutes for deployment

### Step 3: Connect to Cluster
1. **Go to**: Kubernetes services → `ml-housing-cluster`
2. **Click**: "Connect" button
3. **Select**: "Cloud Shell" (browser-based terminal)
4. **Run**: The provided `az acs kubernetes` command
5. **Verify**: `kubectl get nodes` (should show 3 nodes)

### Step 4: Deploy ML API
1. **In Cloud Shell**, create your YAML file:
```bash
cat > ml-housing-api.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-housing-api-deployment
  labels:
    app: ml-housing-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-housing-api
  template:
    metadata:
      labels:
        app: ml-housing-api
    spec:
      containers:
        - name: ml-housing-api
          image: pdharmendra2005/ml-housing-api:withmyvenv
          imagePullPolicy: Always
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "500m"
              memory: "1Gi"
---
apiVersion: v1
kind: Service
metadata:
  name: ml-housing-api-service
spec:
  type: LoadBalancer
  selector:
    app: ml-housing-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-housing-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-housing-api-deployment
  minReplicas: 2
  maxReplicas: 6
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
EOF
```

2. **Deploy**:
```bash
kubectl apply -f ml-housing-api.yaml
```

### Step 5: Monitor Deployment
1. **Check pods**:
```bash
kubectl get pods
```
2. **Check services**:
```bash
kubectl get services
```
3. **Wait for LoadBalancer EXTERNAL-IP** (2-5 minutes)

### Step 6: Test Your ML API
1. **Get external IP** from services output
2. **Test in browser**: `http://<EXTERNAL-IP>/docs`
3. **Test API calls**:
```bash
# Health check
curl http://<EXTERNAL-IP>/

# Model prediction
curl -X POST "http://<EXTERNAL-IP>/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [80000, 5, 7, 3, 20000]}'
```

---

## 🎯 Demo Highlights to Emphasize

### **Portability**
- Same Docker image runs locally AND on Azure
- No code changes needed for cloud deployment

### **Scalability**
- 3 replicas automatically created
- Auto-scaling configured (2-6 replicas)
- LoadBalancer distributes traffic

### **Production Features**
- Resource limits and requests
- Health checks and restarts
- External internet access

### **Cloud Benefits**
- Managed Kubernetes (no maintenance)
- High availability
- Global accessibility

---

## 🔧 Alternative: Azure Container Instances (ACI)

For a **simpler demo** (no Kubernetes):
1. **Search**: "Container instances" → "Create container"
2. **Container settings**:
   - Image: `pdharmendra2005/ml-housing-api:withmyvenv`
   - Port: `8000`
   - DNS name label: `ml-housing-api`
3. **Networking**: Public IP address
4. **Deploy** → Test at `http://<dns-label>.<region>.azurecontainer.io`

---

## 📱 Mobile Demo Tips
- Use Azure mobile app for quick status checks
- Show real-time monitoring in Azure Portal
- Demonstrate scaling by updating replicas

---

## ⚡ Quick Demo Commands
```bash
# Scale up manually
kubectl scale deployment ml-housing-api-deployment --replicas=5

# Check auto-scaling events
kubectl get hpa
kubectl describe hpa ml-housing-api-hpa

# Monitor logs
kubectl logs -f deployment/ml-housing-api-deployment
```

---

## 🎉 Success Metrics for Demo
- ✅ API accessible via public IP
- ✅ Multiple pods running
- ✅ Load balancer working
- ✅ Auto-scaling configured
- ✅ Model predictions working

**Demo Time**: ~15-20 minutes
**Cost**: Minimal (few dollars for demo duration)
