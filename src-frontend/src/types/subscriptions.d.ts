interface MemberSubscription {
  billingCycleAnchor: Date;
  cancelAt: Date;
  cancelAtPeriodEnd: boolean;
  currentPeriodEnd: Date;
  startDate: Date;
  status: string;
}
