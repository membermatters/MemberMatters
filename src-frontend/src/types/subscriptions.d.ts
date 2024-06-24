interface MemberPlan {
  id: number;
  name: string;
  currency: string;
  cost: number;
  intervalAmount: number;
  interval: string;
}

interface MemberTier {
  id: number;
  name: string;
  description: string;
  featured: boolean;
  plans: MemberPlan[];
}

interface MemberSubscription {
  billingCycleAnchor: Date;
  cancelAt: Date;
  cancelAtPeriodEnd: boolean;
  currentPeriodEnd: Date;
  startDate: Date;
  status: string;
  membershipPlan: MemberPlan;
  membershipTier: MemberTier;
}
